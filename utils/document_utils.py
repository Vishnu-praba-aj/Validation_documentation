import json
import re
import pandas as pd

def read_custom_fields(path):
    with open(path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]
    
def export_to_excel(data, output_file="extracted_data.xlsx"):
    metadata_df = pd.DataFrame([data["metadata"]])
    transactions_df = pd.DataFrame(data["transactions"])
    
    with pd.ExcelWriter(output_file) as writer:
        metadata_df.to_excel(writer, sheet_name="Metadata", index=False)
        transactions_df.to_excel(writer, sheet_name="Transactions", index=False)

def clean_json(raw_response):
    cleaned = re.sub(r"^```json\s*|```$", "", raw_response.strip(), flags=re.MULTILINE)
    return cleaned.strip()

def parse_json(response):
    cleaned_json = clean_json(response)
    try:
        return json.loads(cleaned_json)
    except json.JSONDecodeError:
        print("Gemini response is not valid JSON.")
        return {"metadata": {}, "transactions": []}
    