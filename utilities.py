import os
import re

def detect_dynamic_fields(file_content):
    dynamic_patterns = ["setattr(", "__setattr__", "self.__dict__"]
    for pat in dynamic_patterns:
        if pat in file_content:
            return True
    return False

def extract_decorators(file_content):
    return "\n".join(re.findall(r"^\s*@\w+", file_content, re.MULTILINE))

def find_function_definition(func_name, code_files, fetch_content):
    import re
    for file in code_files:
        if file.endswith('.py'):
            content = fetch_content(file)
            match = re.search(
                rf"def {func_name}\s*\(.*\):([\s\S]*?)(?=^def |\Z)", 
                content, 
                re.MULTILINE
            )
            if match:
                return match.group(0)
    return ""

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