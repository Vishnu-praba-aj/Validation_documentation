import ast
import os
import google.generativeai as genai

genai.configure(api_key="AIzaSyA0fL7WUnAHQOE5bIY8pZqqM-Ee0p0lDMA")  # Replace with your Gemini API key



def generate_llm_doc_from_code(file_content):
    prompt = (
        "You are a Python code analysis assistant.\n"
        "Given the following Python code, extract all class fields (attributes) for every class defined in the code. "
        "For each field, explain any validation logic applied to it. "
        "If validation is not explicit, infer possible validation from the code, comments, or docstrings. "
        "Return your answer as a Markdown list, grouped by class and field.\n\n"
        "Python code:\n"
        "'''\n"
        f"{file_content}\n"
        "'''\n"
        "List all fields and their validation logic."
    )
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()

def generate_validation_report(directory):
    report = "# Field Validation Documentation\n\n"
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    file_content = f.read()
                    print(file_content)
                llm_doc = generate_llm_doc_from_code(file_content)
                report += f"## File: {file}\n{llm_doc}\n\n"
    return report

if __name__ == "__main__":
    directory = "."  # Change to your code directory if needed
    doc = generate_validation_report(directory)
    with open("field_validation_documentation.md", "w", encoding="utf-8") as f:
        f.write(doc)
    print("Field validation documentation generated: field_validation_documentation.md")