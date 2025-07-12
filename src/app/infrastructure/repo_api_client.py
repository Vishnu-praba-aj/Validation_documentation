import os
import time
import requests
import fnmatch
from src.app.domain.exception import RepoProcessingException
from utils.logging import setup_logger

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

logger = setup_logger()

class RepoApiClient:
    def is_bitbucket_url(self, url):
        return "bitbucket.org" in url

    def is_github_url(self, url):
        return "github.com" in url

    def parse_repo_url(self, url):
        parts = url.rstrip('/').split('/')
        if len(parts) < 2:
            raise RepoProcessingException("Invalid Repo URL (no user or repo name)")

        owner = parts[-2]
        repo = parts[-1]

        if not owner or not repo:
            raise RepoProcessingException("Invalid Repo URL (no user or repo name)")

        if repo.endswith('.git'):
            repo = repo[:-4]

        return owner, repo

    def is_excluded(self, path):
        norm_path = path.replace("\\", "/")
        for d in EXCLUDED_DIRS:
            if norm_path.startswith(d):
                return True
        base = os.path.basename(norm_path)
        for pattern in EXCLUDED_FILES:
            if fnmatch.fnmatch(base, pattern):
                return True
        return False

    def get_github_default_branch(self, owner, repo):
        url = f"https://api.github.com/repos/{owner}/{repo}"
        resp = requests.get(url)
        if resp.status_code != 200:
            raise RepoProcessingException("No default branch found")
        return resp.json().get('default_branch', 'main')

    def get_github_code_files(self, owner, repo, branch):
        url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
        resp = requests.get(url)
        if resp.status_code != 200:
            raise RepoProcessingException("Could not list GitHub files.")
        data = resp.json()
        files = []
        for item in data.get('tree', []):
            path = item['path']
            if item['type']=='blob' and not self.is_excluded(path):
                files.append(path)
        return files

    def fetch_github_file_content(self, owner, repo, file_path, branch):
        url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{file_path}"
        resp = requests.get(url)
        if resp.status_code != 200:
            raise RepoProcessingException(f"Could not fetch file: {file_path}")
        return resp.text

    def get_bitbucket_default_branch(self, owner, repo):
        url = f"https://api.bitbucket.org/2.0/repositories/{owner}/{repo}"
        resp = requests.get(url)
        if resp.status_code != 200:
            raise RepoProcessingException("No default branch found")
        return resp.json()['mainbranch']['name']

    def get_bitbucket_code_files(self, owner, repo, branch):
        files = []
        url = f"https://api.bitbucket.org/2.0/repositories/{owner}/{repo}/src/{branch}/"
        resp = requests.get(url)
        if resp.status_code != 200:
            raise RepoProcessingException("Could not list Bitbucket files.")
        data = resp.json()
        for item in data.get('values', []):
            path = item['path']
            if not self.is_excluded(path):
                files.append(path)
        while 'next' in data:
            resp = requests.get(data['next'])
            data = resp.json()
            for item in data.get('values', []):
                path = item['path']
                if not self.is_excluded(path):
                    files.append(path)
        return files

    def fetch_bitbucket_file_content(self, owner, repo, file_path, branch):
        url = f"https://bitbucket.org/{owner}/{repo}/raw/{branch}/{file_path}"
        resp = requests.get(url)
        if resp.status_code != 200:
            raise RepoProcessingException(f"Could not fetch file: {file_path}")
        return resp.text

    def get_files_from_repo(self, url):
        start = time.perf_counter()
        if self.is_bitbucket_url(url):
            owner, repo = self.parse_repo_url(url)
            branch = self.get_bitbucket_default_branch(owner, repo)
            code_files = self.get_bitbucket_code_files(owner, repo, branch)
            fetch_content = lambda f: self.fetch_bitbucket_file_content(owner, repo, f, branch)
        elif self.is_github_url(url):
            owner, repo = self.parse_repo_url(url)
            branch = self.get_github_default_branch(owner, repo)
            code_files = self.get_github_code_files(owner, repo, branch)
            fetch_content = lambda f: self.fetch_github_file_content(owner, repo, f, branch)
        elif not (url.startswith("http")):
            raise RepoProcessingException("Not a URL")
        else:
            raise RepoProcessingException("Not a github or bitbucket URL")
        file_objs = []
        for f in code_files:
            file_objs.append({
                "path": f,
                "type": os.path.splitext(f)[1],
                "content": fetch_content(f)
            })
        end = time.perf_counter()
        logger.info(f"Fetched contents from repo in {end - start:.2f} seconds")
        return file_objs