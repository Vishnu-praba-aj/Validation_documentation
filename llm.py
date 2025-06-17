from dotenv import load_dotenv
import os
import google.generativeai as genai
from repo_browser import extract_dependencies
from utilities import find_function_definition

load_dotenv() 
genai_api_key = os.getenv("GENAI_API")

genai.configure(api_key=genai_api_key)

model = genai.GenerativeModel("gemini-1.5-flash")
 
def call_llm(filename, content, decorators,repo,html_content=None):
    dependencies = extract_dependencies(content)
    dep_code_blocks = []
    for dep in dependencies:
        dep_code = find_function_definition(dep,repo)
        if dep_code:
            dep_code_blocks.append(f"# Dependency: {dep}\n{dep_code}")
    prompt_parts = [
    "As an experienced code auditor, your task is to extract all validation logic from the code and format it as a Markdown table.\n"
    ]
    if dep_code_blocks:
        prompt_parts.append(
            "Some validation logic may be implemented in the dependencies listed below.\n\n"
            "Dependency code:" + "\n".join(dep_code_blocks) + "\n"
        )
    if html_content:
        prompt_parts.append(
            "HTML templates associated which may contain validation logic:\n"
            f"{html_content}\n"
        )
    prompt_parts.append(
        f"Source file: '{filename}'\n{content}\n"
        f"Decorators: {decorators}\n"
        "Instructions:\n"
        "1. For each class, object or relevant entity, create a level-2 Markdown heading.\n"
        "2. Under each heading, create a Markdown table summarizing all validation rules for each field. Use columns such as: Field, Required, Type, Min, Max, Email, Pattern, Other Validation.\n"
        "3. Add columns for each validation present in the code. Use 'Other Validation' column for special cases\n"
        "4. Leave cells blank if a constraint is not present for a field.\n"
        "5. Combine validation logic from dependencies, decorators, assertions, comments, utility functions, or HTML templates as needed.\n"
        "6. Do not include any explanation, comments, or code—only Markdown headings and tables.\n"
        "7. Ensure the Markdown tables are properly formatted and render correctly in standard Markdown viewers.\n"
        "Output only the Markdown documentation. Do not include any extra text or explanation."
    )
    prompt = "\n".join(prompt_parts)
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("Error : ", e)
        return "[ERROR] Failed to get response."