from unittest.mock import patch
from src.app.infrastructure.repo_api_client import RepoApiClient

@patch("src.app.infrastructure.repo_api_client.requests.get")
def test_get_github_code_files_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "tree": [{"path": "main.py", "type": "blob"}]
    }
    client = RepoApiClient()
    files = client.get_github_code_files("owner", "repo", "main")
    assert "main.py" in files[0]

def test_is_excluded():
    client = RepoApiClient()
    assert client.is_excluded("node_modules/file.js")
    assert client.is_excluded(".git/config")
    assert not client.is_excluded("src/app.py")
    assert not client.is_excluded("main.java")