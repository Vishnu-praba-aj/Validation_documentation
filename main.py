import os
from input.handler import handle_input
from core.validation_processor import process_validation
from core.document_processor import process_document
from utils.document_utils import export_to_excel, parse_json

OUTPUT_DIR = os.path.join(os.getcwd(), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def main():
    try:
        source = input("Enter repo URL or path to file: ").strip()
        fields = None
        user_prompt = "" 

        if not source.startswith("http"):
            fields = input("Enter path to custom fields .txt: ").strip()
            user_prompt = input("Enter extra prompt instructions (or leave blank): ").strip()

        result = handle_input(source, fields)

        if result["type"] == "code_repo":
            print("Processing repository for validation")
            output_tables = process_validation(result["files"])
            output_path = os.path.join(OUTPUT_DIR, f"{result['repo_name']}_validation.md")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(f"# Validation Documentation: {result['repo_name']}\n\n")
                for table in output_tables:
                    f.write(table + "\n\n")
            print(f"Validation documentation saved at: {output_path}")

        elif result["type"] == "document":
            print("Processing document")
            response = process_document(result["text"], result["fields"], user_prompt)
            json_result = parse_json(response)
            output_path = os.path.join(OUTPUT_DIR, f"{result['filename']}_extracted.xlsx")
            export_to_excel(json_result, output_path)
            print(f"Excel file saved at: {output_path}")

    except FileNotFoundError as fnf_err:
        print(f"File error: {fnf_err}")
    except ValueError as val_err:
        print(f"Input error: {val_err}")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
