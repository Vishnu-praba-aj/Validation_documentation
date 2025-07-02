from core.llm import init_agent_chat
from utils.validation_utils import extract_controller_names, extract_entity_tables, find_htmls_for_controller
from utils.logging import log_duration, setup_logger
import time

logger = setup_logger()

def process_validation(file_objs):
    start = time.perf_counter()
    chat = init_agent_chat("ValidationAgent")
    log_duration(logger, "ValidationAgent chat loading", start)
    
    start = time.perf_counter()
    outputs = []
    html_files = [f for f in file_objs if f["type"] == ".html"]
    fetch_content = lambda p: next(f["content"] for f in file_objs if f["path"] == p)

    all_entity_tables = {}
    entity_usage = {}

    for file in file_objs:
        content = file["content"]
        if file["type"] == ".html":
            continue

        combined_html = ""
        if file["type"] == ".js":
            controller_names = extract_controller_names(content)
            for controller_name in controller_names:
                relevant_htmls = find_htmls_for_controller(
                    controller_name,
                    [h["path"] for h in html_files],
                    fetch_content
                )
                if relevant_htmls:
                    combined_html += "\n".join(relevant_htmls)

        prompt = f"Source file: {file['path']}\n{content}\n"
        if combined_html:
            prompt += f"\nAssociated HTML templates:\n{combined_html}\n"

        log_duration(logger, f"ValidationAgent prompt construction for {file['path']}", start)

        start = time.perf_counter()
        response = chat.send_message(prompt)
        log_duration(logger, f"ValidationAgent response for {file['path']}", start)
        llm_output = response.text.strip()
        outputs.append((file['path'], llm_output))

        entity_tables = extract_entity_tables(llm_output)
        for entity, (etype, table) in entity_tables.items():
            if entity not in all_entity_tables:
                all_entity_tables[entity] = (etype, table)
            entity_usage.setdefault(entity, set()).add(file["path"])

    start = time.perf_counter()
    output_tables = []
    for entity, (etype, table) in all_entity_tables.items():
        if etype == "class":
            output_tables.append(table)
    log_duration(logger, "Post-processing validation output", start)

    return output_tables
