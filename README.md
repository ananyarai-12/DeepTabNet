# DeepTabNet
## Results and Evaluation
### Design Rationale and Techniques Used
🎯 Design Rationale

The design is modular and separates concerns into three key stages:

Document Preprocessing
Converts PDFs to images if needed, so the pipeline can work uniformly on image inputs.

Table Detection
Detects table regions in images using a YOLOv8 model trained on a custom table dataset for accurate and domain-specific detection performance.

Text Recognition and Structuring
Performs OCR to extract text along with their bounding boxes from the detected tables. This spatial information helps in reconstructing structured tables.

Output Generation
Saves the processed results in JSON and CSV formats, with optional cropped table images for review or debugging.

🛠 Techniques Used
1. PDF to Image Conversion
Library: PyMuPDF (fitz)
Purpose: Converts each page of a PDF to PNG for downstream processing.
File: main.py
Function: convert_pdf_to_pngs()

2. Table Detection
Library: ultralytics
Model: YOLOv8, trained on a custom dataset of tables
File: utils.py
Function: detect_tables()
Technique: Returns bounding boxes for detected table regions in input images.

3. Text Recognition and Structuring
Library: PaddleOCR
Files: utils.py
Class: TextRecognizer
Technique:Performs OCR on each detected table region.
Extracts both the text and their respective bounding box coordinates.
This spatial context is used to reconstruct tabular structure accurately.

4. Data Structuring Using LLM
Service: Together API
Model: meta-llama/Llama-4-Scout-17B-16E-Instruct
File: helper.py
Technique:Sends the cropped table image and bounding box text pairs to the LLM.
The model returns a structured JSON object representing table headers and rows.

5. Output Creation
Format: JSON and CSV
File: utils.py
Functions:
create_csv() – converts structured data into a CSV
save_cropped_table_image() – crops and saves images of detected tables
encode_image() – base64-encodes images for LLM input


