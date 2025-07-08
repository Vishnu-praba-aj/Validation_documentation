import os
import base64
import mimetypes
import pandas as pd
import io
from src.app.domain.exception import InvalidFileTypeException

EXTENSION_MIME_MAP = {
    ".csv": "text/csv",
    ".pdf": "application/pdf",
    ".txt": "text/plain",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".xls": "application/vnd.ms-excel"
}

def convert_excel_to_csv_bytes(file_bytes):
    df = pd.read_excel(io.BytesIO(file_bytes))
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    return buffer.getvalue().encode("utf-8")

def read_file_as_part(file_bytes, filename):
    ext = os.path.splitext(filename)[1].lower()
    mime_type = EXTENSION_MIME_MAP.get(ext)

    if not mime_type:
        mime_type, _ = mimetypes.guess_type(filename)
        if not mime_type:
            raise InvalidFileTypeException()

    if ext in [".xlsx", ".xls"]:
        file_bytes = convert_excel_to_csv_bytes(file_bytes)
        mime_type = "text/csv"
    
    return {
        "inline_data": {
            "data": base64.b64encode(file_bytes).decode('utf-8'),
            "mime_type": mime_type
        }
    }