import json
import groq
from typing import Dict
from pathlib import Path

class InteractiveTableAnalyzer:
    def __init__(self, api_key: str, table_data: Dict):
        """
        Initialize with Groq API key and table data.
        
        Args:
            api_key: Your Groq API key
            table_data: Dictionary containing table data (headers and rows)
        """
        self.client = groq.Client(api_key=api_key)
        self.current_model = "llama3-70b-8192"
        self.table_data = table_data
        
        self.system_prompt = """You are a precise table data analyst. Use ONLY the provided table data:

Table Structure:
Headers: {headers}

Data:
{rows_formatted}

Rules:
1. Answer strictly from the table
2. For calculations, show your work
3. Handle non-numeric values appropriately
4. Format dates as in table (e.g., Jan-20)
5. If data isn't available, say "I don't have that information in the table."
6. Be concise but complete"""

    def _format_rows(self) -> str:
        """Format table rows for the prompt."""
        return "\n".join(
            " | ".join(f"{self.table_data['headers'][i]}: {val}" 
                      for i, val in enumerate(row))
            for row in self.table_data["rows"]
        )
    
    def ask(self, question: str) -> str:
        """Ask a question about the table data."""
        try:
            response = self.client.chat.completions.create(
                model=self.current_model,
                messages=[
                    {
                        "role": "system",
                        "content": self.system_prompt.format(
                            headers=", ".join(self.table_data["headers"]),
                            rows_formatted=self._format_rows()
                        )
                    },
                    {"role": "user", "content": question}
                ],
                temperature=0.3,
                max_tokens=1024
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error processing your question: {str(e)}"

def load_table_data(file_path: str) -> Dict:
    """Load table data from JSON file."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Validate the table structure
        if not all(k in data for k in ["headers", "rows"]):
            raise ValueError("JSON must contain 'headers' and 'rows'")
        if len(data["headers"]) != len(data["rows"][0]):
            raise ValueError("Header count doesn't match row columns")
        
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {file_path} was not found")
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format in the data file")

def main():
    """Main interactive interface."""
    print("=== Table Data Analyzer ===")
    
    # Configuration - replace with your actual API key
    API_KEY = "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"
    DATA_FILE = "data.json"  # Path to your JSON data file
    
    # Load table data
    try:
        table_data = load_table_data(DATA_FILE)
        print(f"\nData loaded successfully from {DATA_FILE}")
        print(f"Available columns: {', '.join(table_data['headers'])}")
    except Exception as e:
        print(f"\nFailed to load table data: {str(e)}")
        return
    
    # Initialize analyzer
    analyzer = InteractiveTableAnalyzer(API_KEY, table_data)
    
    # Interactive Q&A loop
    print("\nEnter questions about the table data (type 'exit' to quit)")
    while True:
        question = input("\nYour question: ").strip()
        if question.lower() in ('exit', 'quit'):
            break
        
        if not question:
            print("Please enter a question")
            continue
        
        answer = analyzer.ask(question)
        print(f"\nAnswer: {answer}")
    
    print("\nGoodbye!")

if __name__ == "__main__":
    main()