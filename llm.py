from dotenv import load_dotenv
import os
import google.generativeai as genai
from repo_browser import extract_dependencies
from utilities import find_function_definition

load_dotenv() 
genai_api_key = os.getenv("GENAI_API")

genai.configure(api_key=genai_api_key)

model = genai.GenerativeModel("gemini-1.5-flash")
def test_llm_margin_of_error(call_llm_func, filename, content, decorators, repo, html_content=None, runs=10):
    """
    Runs the LLM multiple times for the same input and calculates the margin of error.
    """
    outputs = []
    for _ in range(runs):
        output = call_llm_func(filename, content, decorators, repo, html_content=html_content)
        outputs.append(output.strip())
    unique_outputs = set(outputs)
    margin_of_error = (len(unique_outputs) - 1) / runs
    print(f"Unique outputs: {len(unique_outputs)} out of {runs} runs")
    print(f"Margin of error: {margin_of_error*100:.2f}%")
    if len(unique_outputs) > 1:
        print("Different outputs:")
        for i, uo in enumerate(unique_outputs, 1):
            print(f"\n--- Output {i} ---\n{uo}\n")
    else:
        print("All outputs are identical.")

def call_llm(filename, content, decorators,repo,code_files, fetch_content,html_content=None):
    dependencies = extract_dependencies(content)
    dep_code_blocks = []
    for dep in dependencies:
        dep_code = find_function_definition(dep, code_files, fetch_content)
        print(f"for dependency: {dep} : {dep_code} in {repo}")
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
        "1. For each class, object or relevant entity without repetition, create a level-2 Markdown heading.\n"
        "2. Under each heading, create a Markdown table summarizing all validation rules for each field. Use columns such as: Field, Required, Type, Min, Max, Default, Pattern, Other Validation.\n"
        "3. Add columns for each validation present in the code. Use 'Other Validation' column for special cases\n"
        "4. Leave cells blank if a constraint is not present for a field.\n"
        "5. Combine validation logic from dependencies, decorators, assertions, comments, utility functions, or HTML templates as needed.\n"
        "6. Ensure the Markdown tables are properly formatted and render correctly in standard Markdown viewers.\n"
    )
    prompt = "\n".join(prompt_parts)
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("Error : ", e)
        return "[ERROR] Failed to get response."