import fitz, pandas as pd

def extract_text_from_file(path):
    if path.endswith(".pdf"):
        doc = fitz.open(path)
        return "".join([page.get_text() for page in doc])
    elif path.endswith(".txt"):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    elif path.endswith((".xls", ".xlsx")):
        return pd.read_excel(path).to_string(index=False)
    raise Exception("Unsupported file format")
