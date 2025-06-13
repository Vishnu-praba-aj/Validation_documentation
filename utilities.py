import json
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

def find_function_definition(func_name, repo_dir):
    for root, _, files in os.walk(repo_dir):
        for file in files:
            if file.endswith('.py'):
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    content = f.read()
                    match = re.search(rf"def {func_name}\s*\(.\):([\s\S]?)(?=^def |\Z)", content, re.MULTILINE)
                    if match:
                        return match.group(0)
    return ""