from core.llm import init_agent_chat
from utils.utilities import parse_json
from utils.logging import log_duration, setup_logger
import time

logger = setup_logger()

def process_document(file, fields, user_prompt=""):
    start = time.perf_counter()
    session_data = init_agent_chat("DocumentAgent", file_path=file)
    chat = session_data["chat"]
    session_id = session_data["session_id"]
    log_duration(logger, "DocumentAgent chat loading", start)

    start = time.perf_counter()
    field_list = ", ".join(fields)
    prompt = f"""Extract the following fields: {field_list}
    {user_prompt.strip() if user_prompt.strip() else ""}
    """
    log_duration(logger, "DocumentAgent Prompt construction", start)

    start = time.perf_counter()
    response = chat.send_message([prompt.strip()])
    log_duration(logger, "DocumentAgent response", start) 

    print("LLM Response:\n", response.text.strip())

    while True:
        cont = input("Do you want to continue the chat with the LLM? (yes/no): ").strip().lower()
        if cont != "yes":
            break
        user_input = input("Enter your message for the LLM: ").strip()
        if not user_input:
            print("No input provided. Exiting chat.")
            break
        start = time.perf_counter()
        response = chat.send_message(user_input)
        log_duration(logger, "DocumentAgent response (interactive)", start)
        print("LLM Response:\n", response.text.strip())

    result = parse_json(response.text)
    return {
        "session_id": session_id,
        "type": "document_extraction",
        "response": result
    }