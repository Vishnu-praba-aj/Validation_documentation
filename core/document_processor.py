from core.llm import init_agent_chat

def process_document(text, fields, user_prompt=""):
    chat = init_agent_chat("DocumentAgent")
    field_list = ", ".join(fields)

    prompt = f"""Extract the following fields: {field_list}
    {user_prompt.strip() if user_prompt.strip() else ""}
    Document:
    {text}"""

    response = chat.send_message(prompt.strip())
    return response.text.strip()