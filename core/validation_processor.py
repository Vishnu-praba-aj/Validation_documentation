from core.llm import init_agent_chat
from utils.validation_utils import extract_controller_names, extract_entity_tables, find_htmls_for_controller

def process_validation(file_objs):
    chat = init_agent_chat("ValidationAgent")
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

        response = chat.send_message(prompt)
        llm_output = response.text.strip()
        outputs.append((file['path'], llm_output))

        entity_tables = extract_entity_tables(llm_output)
        for entity, (etype, table) in entity_tables.items():
            if entity not in all_entity_tables:
                all_entity_tables[entity] = (etype, table)
            entity_usage.setdefault(entity, set()).add(file["path"])

    output_tables = []
    for entity, (etype, table) in all_entity_tables.items():
        if etype == "class":
            output_tables.append(table)

    return output_tables
