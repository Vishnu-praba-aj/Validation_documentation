import fitz  # PyMuPDF
import json
import pandas as pd
import google.generativeai as genai
import os
import re

# === Configure Gemini API ===
genai.configure(api_key="AIzaSyCbGKdpKyOBN678WizJIf1O9viwDpD_Hh0")  # Replace with your actual API key

# === Load the Gemini 1.5 Flash Model ===
model = genai.GenerativeModel("gemini-1.5-flash")

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_txt(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_text_from_excel(excel_path):
    df = pd.read_excel(excel_path)
    return df.to_string(index=False)


def read_custom_fields(fields_txt_path):
    with open(fields_txt_path, 'r', encoding='utf-8') as f:
        fields = [line.strip() for line in f if line.strip()]
    return fields

def get_optional_prompt():
    prompt = input("Enter any extra prompt instructions (or leave blank): ").strip()
    return prompt

def build_llm_prompt(text, custom_fields, user_prompt):
    prompt = """ You are a financial document assistant. Extract the following fields from the input, even if they are phrased differently or use synonyms:
    Return the output strictly in JSON format with two keys:
                    - "metadata": contains the first five fields
                    - "transactions": list of transaction dictionaries
                    If a field is not found, leave it blank.\n"""
    for field in custom_fields:
        prompt += f"- {field}\n"
    if user_prompt:
        prompt += f"\nAdditional instructions: {user_prompt}\n"
    prompt += f"\nHere is the input text:\n{text}\n"
    return prompt



def extract_text(file_path):
    if file_path.lower().endswith(".pdf"):
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
    elif file_path.lower().endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        raise ValueError("Unsupported file type. Use PDF or TXT.")
    return text


def extract_fields_with_gemini(prompt):
    response = model.generate_content(prompt)
    print("Gemini raw response:", response.text)  # Debug: Print raw response from Gemini
    raw_response = response.text 
    cleaned_json = clean_gemini_json(raw_response)
    try:
        return json.loads(cleaned_json)
    except json.JSONDecodeError:
        print("⚠️ Gemini response is not valid JSON.")
        print("Gemini raw response:", response.text)
        return {"metadata": {}, "transactions": []}
    
def clean_gemini_json(raw_response):
    # Remove triple backticks and optional 'json' after them
    cleaned = re.sub(r"^```json\s*|```$", "", raw_response.strip(), flags=re.MULTILINE)
    return cleaned.strip()
    
def export_to_excel(data, output_file="extracted_data.xlsx"):
    metadata_df = pd.DataFrame([data["metadata"]])
    transactions_df = pd.DataFrame(data["transactions"])
    
    with pd.ExcelWriter(output_file) as writer:
        metadata_df.to_excel(writer, sheet_name="Metadata", index=False)
        transactions_df.to_excel(writer, sheet_name="Transactions", index=False)
    print(f"✅ Saved extracted data to {output_file}")

def main():
    input_file = input("Enter the path to your input file (PDF, TXT, or Excel): ").strip()
    fields_file = input("Enter the path to your custom fields .txt file: ").strip()
    user_prompt = get_optional_prompt()

    ext = os.path.splitext(input_file)[1].lower()
    if ext == '.pdf':
        text = extract_text_from_pdf(input_file)
    elif ext == '.txt':
        text = extract_text_from_txt(input_file)
    elif ext in ('.xls', '.xlsx'):
        text = extract_text_from_excel(input_file)
    else:
        print("Unsupported file type.")
        return

    custom_fields = read_custom_fields(fields_file)
    prompt = build_llm_prompt(text, custom_fields, user_prompt)
    print("Prompt sent to LLM:\n", prompt)
    # Call your LLM here (example, replace with your actual call)
    response = extract_fields_with_gemini(prompt)
    #print(response.text)
    print("🧠 Extracted metadata:", response.get("metadata"))
    print("🧾 Sample transactions:", response.get("transactions")[:2])
    export_to_excel(response)
    


main()


