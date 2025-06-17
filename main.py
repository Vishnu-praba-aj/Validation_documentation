from repo_browser import (
    fetch_github_file_content, is_bitbucket_url, is_github_url, parse_repo_url,
    get_github_default_branch, get_github_code_files, 
    get_bitbucket_default_branch, get_bitbucket_code_files, fetch_bitbucket_file_content
)
from utilities import detect_dynamic_fields, extract_controller_names,extract_decorators, find_htmls_for_controller
from llm import call_llm, test_llm_margin_of_error

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
            llm_output = call_llm(file, content, decorators, repo, html_content=combined_html)
            #test_llm_margin_of_error(call_llm, file, content, decorators, repo, html_content=combined_html, runs=10)
        elif file.endswith('.html'):
            continue
        else:
            content = fetch_content(file)
            decorators = extract_decorators(content)
            llm_output = call_llm(file, content, decorators, repo)
            #test_llm_margin_of_error(call_llm, file, content, decorators, repo, runs=10)
        
        if file.endswith('.html'):
            continue
        else:
            formatted_output = f"## {file}\n{llm_output}\n"
            if detect_dynamic_fields(content):
                notes = "> **Note:** This file uses dynamic field creation (e.g., `setattr`). Static analysis may be incomplete."
                formatted_output += f"\n{notes}\n"
            output.append(formatted_output)

    with open(f"{repo}_validation.md", "w", encoding="utf-8") as f:
        f.write(f"# Validation Documentation: {repo}\n\n")
        f.write("\n\n".join(output))
    print(f"Documentation generated: {repo}_validation.md")

if __name__ == "__main__":
    main()
