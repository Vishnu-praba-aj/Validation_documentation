from repo_browser import get_default_branch, get_code_files, fetch_file_content
from utilities import detect_dynamic_fields,extract_decorators
from llm import call_llm

def main():
    url = input("Enter GitHub repo URL (e.g., https://github.com/user/repo): ").strip()
    owner, repo = url.split("/")[-2:]

    branch = get_default_branch(owner, repo)
    code_files = get_code_files(owner, repo, branch)
    llm_output,output = [],[]
    
    for file in code_files:
        content = fetch_file_content(owner, repo, file, branch)
        decorators=extract_decorators(content)
        llm_output=call_llm(file,content,decorators,repo)  
        formatted_output = f"## {file}\n{llm_output}\n"
        if detect_dynamic_fields(content):
            notes = "> **Note:** This file uses dynamic field creation (e.g., `setattr`). Static analysis may be incomplete."
            formatted_output += f"\n{notes}\n\n"
        output.append(formatted_output)

    with open(f"{repo}_validation.md", "w", encoding="utf-8") as f:
        f.write(f"# Validation Documentation: {repo}\n\n")
        f.write("\n\n".join(output))
    print(f"Documentation generated")

if __name__ == "__main__":
    main()
