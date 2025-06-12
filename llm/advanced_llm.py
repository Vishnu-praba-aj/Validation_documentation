import os
import requests
import tempfile
import zipfile
import google.generativeai as genai
import json
import re

genai.configure(api_key="AIzaSyCbGKdpKyOBN678WizJIf1O9viwDpD_Hh0")  # Replace with your Gemini API key

EXCLUDE_EXTENSIONS = (
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".exe", ".dll", ".so", ".zip", ".tar", ".gz", ".rar", ".7z",
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"
)

def get_default_branch(user, repo):
    api_url = f"https://api.github.com/repos/{user}/{repo}"
    r = requests.get(api_url)
    if r.status_code == 200:
        return r.json().get("default_branch", "main")
    raise Exception("Could not determine default branch.")

def download_and_extract_github_repo(repo_url, extract_to):
    if repo_url.endswith('/'):
        repo_url = repo_url[:-1]
    if repo_url.endswith('.git'):
        repo_url = repo_url[:-4]
    parts = repo_url.split('/')
    user, repo = parts[-2], parts[-1]
    branch = get_default_branch(user, repo)
    zip_url = f"https://github.com/{user}/{repo}/archive/refs/heads/{branch}.zip"
    r = requests.get(zip_url)
    if r.status_code != 200 or r.headers.get("Content-Type") != "application/zip":
        raise Exception(f"Could not download repo zip from GitHub. Tried branch: {branch}")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp:
        tmp.write(r.content)
        tmp.flush()
        with zipfile.ZipFile(tmp.name, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    # Return the path to the extracted folder
    extracted_folder = os.path.join(extract_to, os.listdir(extract_to)[0])
    return extracted_folder

def generate_llm_doc_from_code(file_content, filename, repo_dir=None):
    decorators = extract_decorators(file_content)
    # Optionally, find and append utility function code here if needed
    prompt = (
        "You are a code analysis assistant.\n"
        f"The following is the content of a source code file named '{filename}'.\n"
        "For every class or object defined in the code, extract all fields (attributes, properties, or member variables). "
        "For each field, explain any validation logic applied to it, including logic implied by decorators or annotations "
        "(such as @validator, @NotNull, etc.). "
        "If validation is not explicit, infer possible validation from the code, comments, or docstrings. "
        "Return your answer as a Markdown list, grouped by class/object and field.\n\n"
        "Relevant decorators/annotations in this file:\n"
        f"{decorators}\n\n"
        "Source code:\n"
        "'''\n"
        f"{file_content}\n"
        "'''\n"
        "List all fields and their validation logic."
    )
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    result = response.text.strip()
    if detect_dynamic_fields(file_content):
        result += "\n> ⚠️ This file uses dynamic field creation (e.g., setattr). Some fields may not be detected by static analysis."
    return result

def detect_dynamic_fields(file_content):
    dynamic_patterns = ["setattr(", "__setattr__", "self.__dict__"]
    for pat in dynamic_patterns:
        if pat in file_content:
            return True
    return False

def extract_decorators(file_content):
    # Find lines with @decorator
    return "\n".join(re.findall(r"^\s*@\w+", file_content, re.MULTILINE))

def generate_validation_report(directory):
    report = "# Field Validation Documentation\n\n"
    for root, _, files in os.walk(directory):
        for file in files:
            if not file.lower().endswith(EXCLUDE_EXTENSIONS):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        file_content = f.read()
                    llm_doc = generate_llm_doc_from_code(file_content, file)
                    report += f"## File: {os.path.relpath(filepath, directory)}\n{llm_doc}\n\n"
                except Exception as e:
                    report += f"## File: {os.path.relpath(filepath, directory)}\nCould not read file: {e}\n\n"
    return report

def find_function_definition(func_name, repo_dir):
    for root, _, files in os.walk(repo_dir):
        for file in files:
            if file.endswith('.py'):
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    content = f.read()
                    match = re.search(rf"def {func_name}\s*\(.*\):([\s\S]*?)(?=^def |\Z)", content, re.MULTILINE)
                    if match:
                        return match.group(0)
    return ""

if __name__ == "__main__":
    github_repo_url = input("Enter url:").strip()
    print("done")
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_dir = download_and_extract_github_repo(github_repo_url, tmpdir)
        doc = generate_validation_report(repo_dir)
        with open("field_validation_documentation.md", "w", encoding="utf-8") as f:
            f.write(doc)
    print("Field validation documentation generated: field_validation_documentation.md")