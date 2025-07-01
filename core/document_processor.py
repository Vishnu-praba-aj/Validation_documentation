from core.llm import init_agent_chat

def process_document(text, fields, user_prompt=""):
    chat = init_agent_chat("DocumentAgent")
    field_list = ", ".join(fields)

    prompt = f"""Extract the following fields: {field_list}
    {user_prompt.strip() if user_prompt.strip() else ""}
    Document:
    {text}"""

    response = chat.send_message(prompt.strip())
    print("LLM Response:\n", response.text.strip())

    # Interactive chat loop
    while True:
        cont = input("Do you want to continue the chat with the LLM? (yes/no): ").strip().lower()
        if cont != "yes":
            break
        user_input = input("Enter your message for the LLM: ").strip()
        if not user_input:
            print("No input provided. Exiting chat.")
            break
        response = chat.send_message(user_input)
        print("LLM Response:\n", response.text.strip())

    return response.text.strip()