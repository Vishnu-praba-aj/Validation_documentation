from dotenv import load_dotenv
import os
import google.generativeai as genai
from repo_browser import extract_dependencies
from utilities import find_function_definition

load_dotenv() 
genai_api_key = os.getenv("GENAI_API")

genai.configure(api_key=genai_api_key)

model = genai.GenerativeModel("gemini-1.5-flash")
 
def call_llm(filename, content, decorators,repo):
    dependencies = extract_dependencies(content)
    dep_code_blocks = []
    for dep in dependencies:
        dep_code = find_function_definition(dep,repo)
        if dep_code:
            dep_code_blocks.append(f"# Dependency: {dep}\n{dep_code}")
    prompt = (
        "As an experienced code auditing assistant, analyze the following code and format the output in proper Markdown syntax.\n\n"
        "Dependency code:\n" + "\n\n".join(dep_code_blocks) + "\n\n"
        f"Source file: '{filename}'\n{content}\n\n"
        f"Decorators: {decorators}\n\n"
        "This code may have been written many years ago and may use legacy or procedural patterns.\n"
        "Some validation logic may be implemented in the dependencies listed below.\n\n"
        "Your task is to extract all validation logic from the code and format it as a Markdown table.\n"
        "Instructions:\n"
        "1.For each class/object, create a level-2 heading with its name:\n"
        "2.Under each heading, create a properly formatted Markdown table:\n"
        "-Use standard Markdown table syntax with aligned columns\n"
        "-Include header separator row with proper alignment indicators\n"
        "-Example format:\n"
        "-| Field | Type | Required | Min | Max | Other Validation |\n"
        "3.Table requirements:\n"
        "-First column must be 'Field'\n"
        "-For every class or object defined in the code, extract all fields (attributes, properties, or member variables) and their validation logic, including logic from dependencies, decorators, assertions, comments, or utility functions"
        "-Add columns for each validation present in the code\n"
        "-Use 'Other Validation' column for special cases\n"
        "-Leave cells blank when constraint absent\n"
        "-Ensure proper cell spacing and alignment\n\n"
        "-No explanatory text or implementation details\n"
    )
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("Error : ", e)
        return "[ERROR] Failed to get response."