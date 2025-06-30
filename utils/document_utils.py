import json
import re
import pandas as pd

def read_custom_fields(path):
    with open(path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]
    
def export_to_excel(data, output_file="extracted_data.xlsx"):
    user_fields = data.get("user_fields", [])
    doc_fields = data.get("document_fields", [])
    values = data.get("values", [])

    # Ensure all values are lists of the same length (pad with empty strings if needed)
    max_len = max([len(v) if isinstance(v, list) else 1 for v in values] + [1])
    value_rows = []
    for i in range(max_len):
        row = []
        for v in values:
            if isinstance(v, list):
                row.append(v[i] if i < len(v) else "")
            else:
                row.append(v if i == 0 else "")
        value_rows.append(row)

    # Build the DataFrame rows
    rows = []

    # First row: CustomFields
    rows.append(["CustomFields"] + user_fields)
    # Second row: Label (document_fields)
    rows.append(["Label"] + doc_fields)
    # Data rows: values with Ref as blank or auto-number
    for idx, val_row in enumerate(value_rows, 1):
        rows.append([str(idx)] + val_row)

    df = pd.DataFrame(rows)
    with pd.ExcelWriter(output_file) as writer:
        df.to_excel(writer, sheet_name="Extracted Fields", index=False, header=False)

def clean_json(raw_response):
    cleaned = re.sub(r"^```json\s*|```$", "", raw_response.strip(), flags=re.MULTILINE)
    return cleaned.strip()

def parse_json(response):
    cleaned_json = clean_json(response)
    try:
        return json.loads(cleaned_json)
    except json.JSONDecodeError:
        print("Gemini response is not valid JSON.")
        # Return empty lists for the three keys as per new prompt
        return {"user_fields": [], "document_fields": [], "values": []}
