import os
import time
from input.handler import handle_input
from core.validation_processor import process_validation
from core.document_processor import process_document,process_doc
from utils.document_utils import export_to_excel, parse_json
from utils.logging import setup_logger, log_duration

OUTPUT_DIR = os.path.join(os.getcwd(), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)
logger = setup_logger()  

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
            logger.info("Processing repository for validation")
            output_tables = process_validation(result["files"])
            output_path = os.path.join(OUTPUT_DIR, f"{result['repo_name']}_validation.md")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(f"# Validation Documentation: {result['repo_name']}\n\n")
                for table in output_tables:
                    f.write(table + "\n\n")
            print(f"Validation documentation saved at: {output_path}")

        elif result["type"] == "document":
            print("Processing document")
            logger.info("Processing document")
            response = process_doc(source, result["fields"], user_prompt) 
            logger.info("Processing complete. Extracting fields...")
            print("Processing complete. Extracting fields...",response)
            start = time.perf_counter()
            json_result = parse_json(response)
            log_duration(logger, "Post processing output from LLM", start)
            output_path = os.path.join(OUTPUT_DIR, f"{result['filename']}_extracted.xlsx")
            export_to_excel(json_result, output_path)
            logger.info(f"Excel file saved at: {output_path}")
            print(f"Excel file saved at: {output_path}")

    except FileNotFoundError as fnf_err:
        logger.error(f"File error: {fnf_err}")
        print(f"File error: {fnf_err}")
    except ValueError as val_err:
        logger.error(f"Input error: {val_err}")
        print(f"Input error: {val_err}")
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        print(f"Unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
