from repo_browser import (
    fetch_github_file_content, is_bitbucket_url, is_github_url, parse_repo_url,
    get_github_default_branch, get_github_code_files, 
    get_bitbucket_default_branch, get_bitbucket_code_files, fetch_bitbucket_file_content
)
from utilities import detect_dynamic_fields,extract_decorators
from llm import call_llm

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
    
    for file in code_files:
        content = fetch_content(file)
        decorators=extract_decorators(content)
        llm_output=call_llm(file,content,decorators,repo)  
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
