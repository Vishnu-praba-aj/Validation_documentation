import google.generativeai as genai
from utils.config import GENAI_API_KEY, LLM_MODEL

genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel(LLM_MODEL)

def test_llm_margin_of_error(call_llm_func, filename, content, html_content=None, runs=10):
    outputs = []
    for _ in range(runs):
        output = call_llm_func(filename, content, html_content=html_content)
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

def call_llm(filename, content, html_content=None):
    prompt_parts = [
        "As an experienced code auditor, your task is to extract all validation logic from the code and format it as a Markdown table.\n"
    ]
    if html_content:
        prompt_parts.append(
            "HTML templates associated which may contain validation logic:\n"
            f"{html_content}\n"
        )
    prompt_parts.append(
        f"Source file: '{filename}'\n{content}\n"
        "Instructions:\n"
        "1. For each class, object or relevant entity without repetition, create a level-2 Markdown heading.\n"
        "2. Under each heading, create a Markdown table summarizing all validation rules for each field.Include fields with no validation too. Use columns such as: Field, Required, Type, Min, Max,Length, Default, Pattern, Other Validation.\n"
        "3. Add columns for each validation present in the code. Use 'Other Validation' column for special cases\n"
        "4. Leave cells blank if a constraint is not present for a field.\n"
        "5. Combine validation logic from dependencies, decorators, assertions, comments, utility functions, or HTML templates as needed.\n"
        "6. Ensure the Markdown tables are properly formatted and render correctly in standard Markdown viewers.\n"
        "7. Be consistent in the responses. Always use Yes or No for required column. Type should be a single word, e.g., String, Integer, Boolean, etc\n"
        "8. Do not include any code snippets, explanations or summary only the Markdown table.\n"
    )
    prompt = "\n".join(prompt_parts)
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("Error : ", e)
        return "[ERROR] Failed to get response."