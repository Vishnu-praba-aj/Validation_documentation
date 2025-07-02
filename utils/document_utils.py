import json
import re
import pandas as pd

def read_custom_fields(path):
    with open(path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]
    
def export_to_excel(data, output_file="extracted_data.xlsx"):
    custom_fields = data.get("user_fields", [])
    label = data.get("document_fields", [])
    values = data.get("values", [])

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

    rows = []

    rows.append(["CustomFields"] + custom_fields)
    rows.append(["Label"] + label)
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
        return {"user_fields": [], "document_fields": [], "values": []}
