# You need to install requests: pip install requests
import requests
import base64
import fnmatch

EXCLUDE_PATTERNS = [
    "__pycache__",
    "*.class",
    "*.o",
    "*.exe",
    "*.dll",
    "*.so",
    "*.log",
    "*.tmp",
    ".DS_Store",
    ".gitignore",
    ".env",
    ".venv",
    ".idea",
    ".vscode",
    "*.ipynb_checkpoints",
    "*.md"
]

def is_excluded(filename):
    for pattern in EXCLUDE_PATTERNS:
        if fnmatch.fnmatch(filename, pattern) or f"/{pattern.strip('*')}/" in filename:
            return True
    return False

def list_files(owner, repo, path=""):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

def print_files_recursive(owner, repo, path="", excluded=None):
    if excluded is None:
        excluded = []
    items = list_files(owner, repo, path)
    for item in items:
        if is_excluded(item['path']):
            excluded.append(item['path'])
            continue
        if item['type'] == 'file':
            print(f"\n--- {item['path']} ---")
            file_resp = requests.get(item['download_url'])
            file_resp.raise_for_status()
            print(file_resp.text[:500])  # Print first 500 chars
        elif item['type'] == 'dir':
            print_files_recursive(owner, repo, item['path'], excluded)
    return excluded

if __name__ == "__main__":
    owner = "Vishnu-praba-aj"  # Replace with the repo owner
    repo = "Lab2repo"  # Replace with the repo name
    excluded_files = print_files_recursive(owner, repo)
    if excluded_files:
        print("\nExcluded files/directories:")
        for f in excluded_files:
            print(f"- {f}")
    else:
        print("\nNo files were excluded.")