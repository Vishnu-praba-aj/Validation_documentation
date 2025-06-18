from repo_browser import (
    fetch_github_file_content, is_bitbucket_url, is_github_url, parse_repo_url,
    get_github_default_branch, get_github_code_files, 
    get_bitbucket_default_branch, get_bitbucket_code_files, fetch_bitbucket_file_content
)
from utilities import detect_dynamic_fields, extract_controller_names,extract_decorators, find_htmls_for_controller
from llm import call_llm, test_llm_margin_of_error
import re

def extract_entity_tables(llm_output):
    """
    Extracts tables for each entity/class/function from the LLM output.
    Returns a dict: {entity_name: (entity_type, table_markdown)}
    """
    lines = llm_output.splitlines()
    entity_tables = {}
    current_entity = None
    current_type = None
    buffer = []
    for line in lines:
        # Match headings like "## Person" or "## `validate_age` function"
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

def main():
    url = input("Enter a repo URL : ").strip()
    owner, repo = parse_repo_url(url)
    if is_bitbucket_url(url):
        branch = get_bitbucket_default_branch(owner, repo)
        code_files = get_bitbucket_code_files(owner, repo, branch)
        fetch_content = lambda f: fetch_bitbucket_file_content(owner, repo, f, branch)
    elif is_github_url(url):
        branch = get_github_default_branch(owner, repo)
        code_files = get_github_code_files(owner, repo, branch)
        fetch_content = lambda f: fetch_github_file_content(owner, repo, f, branch)
    else:
        print("Unsupported URL. Please provide a GitHub or Bitbucket repository URL.")
        return

    output = []
    html_files = [f for f in code_files if f.endswith('.html')]

    all_entity_tables = {}
    entity_usage = {}  # Track where each entity is used

    for file in code_files:
        if file.endswith('.js'):
            content = fetch_content(file)
            decorators = extract_decorators(content)
            controller_names = extract_controller_names(content)
            combined_html = ""
            for controller_name in controller_names:
                relevant_htmls = find_htmls_for_controller(controller_name, html_files,fetch_content)
                if relevant_htmls:
                    combined_html += "\n".join(relevant_htmls)
            llm_output = call_llm(file, content, decorators, repo,code_files, fetch_content, html_content=combined_html)
            #test_llm_margin_of_error(call_llm, file, content, decorators, repo, html_content=combined_html, runs=10)
        elif file.endswith('.html'):
            continue
        else:
            content = fetch_content(file)
            decorators = extract_decorators(content)
            llm_output = call_llm(file, content, decorators, repo,code_files, fetch_content)
            #test_llm_margin_of_error(call_llm, file, content, decorators, repo, runs=10)
        
        if file.endswith('.html'):
            continue
        else:
            formatted_output = f"## {file}\n{llm_output}\n"
            if detect_dynamic_fields(content):
                notes = "> **Note:** This file uses dynamic field creation (e.g., `setattr`). Static analysis may be incomplete."
                formatted_output += f"\n{notes}\n"
            output.append(formatted_output)

        entity_tables = extract_entity_tables(llm_output)
        for entity, (etype, table) in entity_tables.items():
            if entity not in all_entity_tables:
                all_entity_tables[entity] = (etype, table)
            # Track usage (for dependency analysis)
            entity_usage.setdefault(entity, set()).add(file)

    # Now, only output tables for classes/entities, not for helper functions
    output_tables = []
    for entity, (etype, table) in all_entity_tables.items():
        if etype == "class":
            output_tables.append(table)
        # Optionally, if a function is not used as a dependency, you can include it:
        # elif etype == "function" and len(entity_usage[entity]) > 1:
        #     output_tables.append(table)

    with open(f"{repo}_validation.md", "w", encoding="utf-8") as f:
        f.write(f"# Validation Documentation: {repo}\n\n")
        for table in output_tables:
            f.write(table + "\n\n")
    print(f"Documentation generated: {repo}_validation.md")

if __name__ == "__main__":
    main()
