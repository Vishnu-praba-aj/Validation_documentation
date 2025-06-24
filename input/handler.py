import os
from input.repo_browser import get_files_from_repo
from input.file_input import extract_text_from_file
from utils.document_utils import read_custom_fields

def handle_input(input_path_or_url, fields_txt=None):
    if input_path_or_url.startswith("http"):
        files = get_files_from_repo(input_path_or_url)
        return {
            "type": "code_repo",
            "repo_name": input_path_or_url.rstrip("/").split("/")[-1],
            "files": files
        }
    else:
        if not fields_txt:
            raise ValueError("Field definitions .txt path is required for document input.")
        
        if not os.path.exists(fields_txt):
            raise FileNotFoundError(f"Custom fields file not found: {fields_txt}")

        text = extract_text_from_file(input_path_or_url)
        fields = read_custom_fields(fields_txt)
        filename = os.path.splitext(os.path.basename(input_path_or_url))[0]
        return {
            "type": "document",
            "text": text,
            "fields": fields,
            "filename": filename
        }