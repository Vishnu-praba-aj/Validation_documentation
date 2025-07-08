import json
import re
from src.app.domain.exception import JSONParsingException
from utils.logging import setup_logger

logger = setup_logger()

def clean_json(raw_response):
    cleaned = re.sub(r"^```json\s*|```$", "", raw_response.strip(), flags=re.MULTILINE)
    return cleaned

def parse_json(response):
    cleaned_json = clean_json(response)
    try:
        return json.loads(cleaned_json)
    except json.JSONDecodeError:
        raise JSONParsingException()

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
