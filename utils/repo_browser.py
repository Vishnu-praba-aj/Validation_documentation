import os
import requests
import fnmatch

EXCLUDED_DIRS = [
    ".venv/", "venv/", "env/", "virtualenv/",
    "node_modules/", "bower_components/", "jspm_packages/",
    ".git/", ".svn/", ".hg/", ".bzr/","__pycache__/",
    "environments/", "e2e/"
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
    'angular.json', 'tsconfig.json', 'tsconfig.app.json', 'tsconfig.spec.json',
    'tslint.json', 'karma.conf.js', 'package.json', 'package-lock.json',
    '.editorconfig', '.browserslistrc', 'README.md'
]

def is_bitbucket_url(url):
    return "bitbucket.org" in url

def is_github_url(url):
    return "github.com" in url

def parse_repo_url(url):
    parts = url.rstrip('/').split('/')
    owner = parts[-2]
    repo = parts[-1]
    if repo.endswith('.git'):
        repo = repo[:-4]
    return owner, repo

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

def get_github_default_branch(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    resp = requests.get(url)
    if resp.status_code != 200:
        raise Exception("Could not determine default branch.")
    return resp.json().get('default_branch', 'main')

def get_github_code_files(owner, repo, branch):
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    resp = requests.get(url)
    if resp.status_code != 200:
        raise Exception("Could not list files.")
    data = resp.json()
    files = []
    for item in data.get('tree', []):
        path = item['path']
        if item['type']=='blob' and not is_excluded(path):
            files.append(path)
    return files

def fetch_github_file_content(owner, repo, file_path, branch):
    url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{file_path}"
    resp = requests.get(url)
    if resp.status_code != 200:
        raise Exception(f"Could not fetch file: {file_path}")
    return resp.text

def get_bitbucket_default_branch(owner, repo):
    url = f"https://api.bitbucket.org/2.0/repositories/{owner}/{repo}"
    resp = requests.get(url)
    if resp.status_code != 200:
        raise Exception("Could not determine Bitbucket default branch.")
    return resp.json()['mainbranch']['name']

def get_bitbucket_code_files(owner, repo, branch):
    files = []
    url = f"https://api.bitbucket.org/2.0/repositories/{owner}/{repo}/src/{branch}/"
    resp = requests.get(url)
    if resp.status_code != 200:
        raise Exception("Could not list Bitbucket files.")
    data = resp.json()
    for item in data.get('values', []):
        path = item['path']
        if not is_excluded(path):
            files.append(path)
    while 'next' in data:
        resp = requests.get(data['next'])
        data = resp.json()
        for item in data.get('values', []):
            path = item['path']
            if not is_excluded(path):
                files.append(path)
    return files

def fetch_bitbucket_file_content(owner, repo, file_path, branch):
    url = f"https://bitbucket.org/{owner}/{repo}/raw/{branch}/{file_path}"
    resp = requests.get(url)
    if resp.status_code != 200:
        raise Exception(f"Could not fetch file: {file_path}")
    return resp.text