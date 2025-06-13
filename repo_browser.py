import os
import re
import requests
import fnmatch

EXCLUDED_DIRS = [
    ".venv/", "venv/", "env/", "virtualenv/",
    "node_modules/", "bower_components/", "jspm_packages/",
    ".git/", ".svn/", ".hg/", ".bzr/","__pycache__/",
]

EXCLUDED_FILES = [
    "yarn.lock", "pnpm-lock.yaml", "npm-shrinkwrap.json", "poetry.lock",
    "Pipfile.lock", "requirements.txt.lock", "Cargo.lock", "composer.lock",
    ".DS_Store", "Thumbs.db", "desktop.ini", ".env", ".gitignore",
    "*.lock", "*.lnk", "*.min.js", "*.min.css", "*.bundle.js", "*.map",
    "*.gz", "*.zip", "*.tar", "*.rar", "*.7z", "*.iso", "*.dmg",
    "*.exe", "*.dll", "*.so", "*.pyd", "*.class", "*.jar", "*.war",
    "__pycache__", "*.pyc", "*.egg", "*.dist-info", "*.a", "*.lib",
    "dist/", "build/", "coverage/", ".tox/", "node_modules/","__init__.py",
    "package-lock.json", "yarn-error.log", "yarn.lock", "pnpm-lock.yaml",
]

def is_excluded(path):
    norm_path = path.replace("\\", "/")

    for d in EXCLUDED_DIRS:
        if norm_path.startswith(d):
            return True

    base = os.path.basename(norm_path)
    for pattern in EXCLUDED_FILES:
        if fnmatch.fnmatch(base, pattern):
            return True

    return False

def get_default_branch(user, repo):
    api_url = f"https://api.github.com/repos/{user}/{repo}"
    r = requests.get(api_url)
    if r.status_code == 200:
        return r.json().get("default_branch", "main")
    raise Exception("Could not determine default branch.")

def get_code_files(owner, repo, branch):
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    response = requests.get(url)
    response.raise_for_status()
    tree = response.json()["tree"]
    return [
        f["path"] for f in tree
        if f["type"] == "blob"
        and f["path"].endswith(('.py', '.js', '.java'))
        and not is_excluded(f["path"])
    ]

def fetch_file_content(owner, repo, file_path, branch):
    url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{file_path}"
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def extract_dependencies(file_content):
    imports = re.findall(r'from\s+(\S+)\s+import\s+(\w+)', file_content)
    used = set()
    for _, name in imports:
        used.add(name)
    used.update(re.findall(r'@(\w+)', file_content))
    used.update(re.findall(r'(\w+)\(', file_content))
    return used