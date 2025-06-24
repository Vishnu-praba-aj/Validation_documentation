from core.llm import init_agent_chat

def process_document(text, fields, user_prompt=""):
    chat = init_agent_chat("DocumentAgent")
    field_list = "\n".join(f"- {f}" for f in fields)
    prompt = f"Extract the following fields:\n{field_list}\n{user_prompt}\n\nExtract from this:\n{text}"
    response = chat.send_message(prompt)
    return response.text.strip()