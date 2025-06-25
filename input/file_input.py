import fitz, pandas as pd

def extract_text_from_file(path):
    if path.endswith(".pdf"):
        try:
            doc = fitz.open(path)
            return "".join([page.get_text() for page in doc])
        except Exception as e:
            raise ValueError(f"Failed to extract text from PDF: {e}")

    elif path.endswith(".txt"):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            raise ValueError(f"Failed to read text file: {e}")

    elif path.endswith((".xls", ".xlsx")):
        try:
            return pd.read_excel(path).to_string(index=False)
        except Exception as e:
            raise ValueError(f"Failed to extract from Excel: {e}")

    raise Exception(f"Unsupported file format: {path}")
