from src.app.infrastructure.file_handler import read_file_as_part, convert_excel_to_csv_bytes
import pandas as pd
import io
import pytest

def test_get_mime_type_from_filename_csv():
    part = read_file_as_part(b"col1,col2\n1,2", "test.csv")
    assert part["inline_data"]["mime_type"] == "text/csv"

def test_get_mime_type_from_filename_pdf():
    part = read_file_as_part(b"%PDF-1.4", "test.pdf")
    assert part["inline_data"]["mime_type"] == "application/pdf"

def test_unsupported_file_type():
    with pytest.raises(ValueError):
        read_file_as_part(b"dummy", "test.unknown")

def test_excel_to_csv_conversion_valid():
    df = pd.DataFrame({"a": [1,2], "b": [3,4]})
    buffer = io.BytesIO()
    df.to_excel(buffer, index=False, engine="openpyxl")
    buffer.seek(0)
    csv_bytes = convert_excel_to_csv_bytes(buffer.getvalue())
    assert b"a,b" in csv_bytes

def test_excel_to_csv_conversion_invalid():
    with pytest.raises(Exception):
        convert_excel_to_csv_bytes(b"not an excel file")