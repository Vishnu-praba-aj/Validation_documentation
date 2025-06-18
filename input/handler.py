from utils.repo_browser import (
    fetch_github_file_content, fetch_bitbucket_file_content,
    is_bitbucket_url, is_github_url, parse_repo_url,
    get_github_default_branch, get_github_code_files,
    get_bitbucket_default_branch, get_bitbucket_code_files
)
import os

def get_files_from_repo(url):
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
        raise Exception("Unsupported repo URL")
    file_objs = []
    for f in code_files:
        file_objs.append({
            "path": f,
            "type": os.path.splitext(f)[1],
            "content": fetch_content(f)
        })
    return file_objs

def get_input_files(source):
    if source.startswith("http"):
        return get_files_from_repo(source)
    else:
        raise NotImplementedError("Only repo URLs are supported")