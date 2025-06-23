import re

def extract_controller_names(js_content):
    return re.findall(r"\.controller\(['\"](\w+)['\"]", js_content)

def find_htmls_for_controller(controller_name, html_files, fetch_content):
    relevant_htmls = []
    pattern = re.compile(r'ng-controller\s*=\s*[\'"]' + re.escape(controller_name) + r'[\'"]', re.IGNORECASE)
    for html_file in html_files:
        html_content = fetch_content(html_file)
        if pattern.search(html_content):
            relevant_htmls.append(html_content)
    return relevant_htmls

def extract_entity_tables(llm_output):
    lines = llm_output.splitlines()
    entity_tables = {}
    current_entity = None
    current_type = None
    buffer = []
    for line in lines:
        m = re.match(r"^##\s+`?(\w+)`?(?: function)?", line)
        if m:
            if current_entity and buffer:
                entity_tables[current_entity] = (current_type, "\n".join(buffer))
            current_entity = m.group(1)
            current_type = "function" if "function" in line else "class"
            buffer = [line]
        else:
            buffer.append(line)
    if current_entity and buffer:
        entity_tables[current_entity] = (current_type, "\n".join(buffer))
    return entity_tables