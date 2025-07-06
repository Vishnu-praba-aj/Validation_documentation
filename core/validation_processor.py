from core.llm import init_agent_chat
from utils.utilities import parse_json
from utils.utilities import extract_controller_names, find_htmls_for_controller
from utils.logging import log_duration, setup_logger
import time

logger = setup_logger()
MAX_CHUNK_SIZE = 1500

def chunk_text(text):
    for i in range(0, len(text), MAX_CHUNK_SIZE):
        yield text[i:i + MAX_CHUNK_SIZE]

def process_validation(file_objs):
    start = time.perf_counter()
    session_data = init_agent_chat("ValidationAgent")
    chat = session_data["chat"]
    session_id = session_data["session_id"]
    log_duration(logger, "ValidationAgent chat loading", start)
    
    html_files = {f["path"]: f["content"] for f in file_objs if f["type"] == ".html"}
    code_blocks = []

    for file in file_objs:
        if file["type"] == ".html":
            continue

        content = file["content"]
        file_block = f"\nFile: {file['path']}\n{content}"

        if file["type"] == ".js":
            controller_names = extract_controller_names(content)
            associated_html = []
            for controller_name in controller_names:
                matched_html = find_htmls_for_controller(controller_name, html_files.keys(), html_files.get)
                if matched_html:
                    associated_html.extend(matched_html)
            if associated_html:
                file_block += f"\nAssociated HTML:\n" + "\n".join(associated_html)

        code_blocks.append(file_block)

    full_code_text = "\n".join(code_blocks)
    chunks = list(chunk_text(full_code_text))

    for idx, chunk in enumerate(chunks):
        prompt = f"Code Chunk {idx + 1} of {len(chunks)}:\n{chunk}"
        start = time.perf_counter()
        chat.send_message(prompt)
        log_duration(logger, f"ValidationAgent context chunk {idx+1} sent", start)

    final_prompt = (
        "You have now received all code and associated HTML files.\n"
        "Using ALL the code and HTML files provided, extract all validation logic as per the instructions."
    )
    start = time.perf_counter()
    response = chat.send_message(final_prompt)
    log_duration(logger, "ValidationAgent Response", start)

    llm_output = response.text.strip()
    output = parse_json(llm_output)

    print("Validation output:\n", output)
    return {
        "session_id": session_id,
        "type": "validation_result",
        "response": output
    }