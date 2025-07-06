import base64
import io
import os
import pandas as pd

EXTENSION_MIME_MAP = {
    ".csv": "text/csv",
    ".pdf": "application/pdf",
    ".txt": "text/plain",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".xls": "application/vnd.ms-excel",
}

def read_custom_fields(path):
    with open(path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def convert_excel_to_csv_bytes(file_path):
    df = pd.read_excel(file_path, engine='openpyxl')
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    return buffer.getvalue().encode("utf-8")

def read_file_as_part(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()
    mime_type = EXTENSION_MIME_MAP.get(ext)

    if not mime_type:
        raise ValueError(f"Unsupported file type: {ext}")

    if ext in [".xlsx", ".xls"]:
        data = convert_excel_to_csv_bytes(file_path)
        mime_type = "text/csv" 
    else:
        with open(file_path, "rb") as f:
            data = f.read()

    return {
        "inline_data": {
            "data": base64.b64encode(data).decode('utf-8'),
            "mime_type": mime_type
        }
    }