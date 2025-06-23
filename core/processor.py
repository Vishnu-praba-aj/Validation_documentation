from core.llm import call_llm
from utils.utilities import (
    extract_controller_names, find_htmls_for_controller, extract_entity_tables
)

def process_files(file_objs):
    output = []
    html_files = [f for f in file_objs if f["type"] == ".html"]

    fetch_content = lambda p: next(f["content"] for f in file_objs if f["path"] == p)

    all_entity_tables = {}
    entity_usage = {}

    for file in file_objs:
        content = file["content"]
        if file["type"] == ".html":
            continue
        
        if file["type"] == ".js":
            controller_names = extract_controller_names(content)
            combined_html = ""
            for controller_name in controller_names:
                relevant_htmls = find_htmls_for_controller(
                    controller_name,
                    [h["path"] for h in html_files],
                    fetch_content
                )
                if relevant_htmls:
                    combined_html += "\n".join(relevant_htmls)
            llm_output = call_llm(file["path"], content, html_content=combined_html)
        else:
            llm_output = call_llm(file["path"], content)
        
        formatted_output = f"## {file['path']}\n{llm_output}\n"
        output.append(formatted_output)

        entity_tables = extract_entity_tables(llm_output)
        for entity, (etype, table) in entity_tables.items():
            if entity not in all_entity_tables:
                all_entity_tables[entity] = (etype, table)
            entity_usage.setdefault(entity, set()).add(file["path"])

    output_tables = []
    for entity, (etype, table) in all_entity_tables.items():
        if etype == "class":
            output_tables.append(table)
        # Optionally, include functions used in multiple files:
        # elif etype == "function" and len(entity_usage[entity]) > 1:
        #     output_tables.append(table)
    
    return output_tables