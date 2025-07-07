import pytest
from httpx import AsyncClient
from unittest.mock import patch, MagicMock
from src.app.api.main import app

# --- VALIDATION ENDPOINT TESTS ---

@pytest.mark.asyncio
@patch("src.app.infrastructure.repo_api_client.RepoApiClient.get_files_from_repo")
@patch("src.app.infrastructure.llm_client.LLMClient.start_session")
async def test_analyze_repo_success(mock_start_session, mock_get_files):
    """
    Test /validation/analyze_repo/ with a valid repo_url.
    Should return 200 and a valid validation response structure.
    """
    mock_get_files.return_value = [
        {"path": "main.py", "type": ".py", "content": "print(1)"}
    ]
    mock_chat = MagicMock()
    mock_chat.send_message.return_value.text = '{"entities": [{"name": "User", "fields": []}]}'
    mock_start_session.return_value = ("sid", mock_chat)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/validation/analyze_repo/", json={"repo_url": "https://github.com/owner/repo"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["session_id"] == "sid"
        assert data["type"] == "validation"
        assert "entities" in data["response"]

@pytest.mark.asyncio
@patch("src.app.infrastructure.repo_api_client.RepoApiClient.get_files_from_repo")
async def test_analyze_repo_invalid_url(mock_get_files):
    """
    Test /validation/analyze_repo/ with an invalid repo_url.
    Should return 400 or 500 error.
    """
    mock_get_files.side_effect = Exception("Invalid repo url")
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/validation/analyze_repo/", json={"repo_url": "invalid"})
        assert resp.status_code in (400, 500)

@pytest.mark.asyncio
@patch("src.app.infrastructure.repo_api_client.RepoApiClient.get_files_from_repo")
@patch("src.app.infrastructure.llm_client.LLMClient.start_session")
async def test_analyze_repo_llm_malformed_json(mock_start_session, mock_get_files):
    """
    Test /validation/analyze_repo/ where LLM returns malformed JSON.
    Should return 500 error.
    """
    mock_get_files.return_value = [
        {"path": "main.py", "type": ".py", "content": "print(1)"}
    ]
    mock_chat = MagicMock()
    mock_chat.send_message.return_value.text = "not a json"
    mock_start_session.return_value = ("sid", mock_chat)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/validation/analyze_repo/", json={"repo_url": "https://github.com/owner/repo"})
        assert resp.status_code == 500

# --- DOCUMENT EXTRACTION ENDPOINT TESTS ---

@pytest.mark.asyncio
@patch("src.app.infrastructure.llm_client.LLMClient.start_session")
async def test_extract_fields_success(mock_start_session):
    """
    Test /document/extract_fields/ with valid Excel and fields files.
    Should return 200 and a valid extraction response structure.
    """
    mock_chat = MagicMock()
    mock_chat.send_message.return_value.text = '{"response": {"rows": [{"index": 0, "fields": []}]}}'
    mock_start_session.return_value = ("sid", mock_chat)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        files = {
            "doc": ("test.xlsx", b"dummyexcelbytes", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
            "custom_fields": ("fields.txt", b"field1\nfield2", "text/plain"),
        }
        data = {"user_prompt": "Extract all fields"}
        resp = await ac.post("/document/extract_fields/", files=files, data=data)
        assert resp.status_code == 200
        data = resp.json()
        assert data["session_id"] == "sid"
        assert data["type"] == "document_extraction"
        assert "rows" in data["response"]

@pytest.mark.asyncio
@patch("src.app.infrastructure.llm_client.LLMClient.start_session")
async def test_extract_fields_unsupported_file_type(mock_start_session):
    """
    Test /document/extract_fields/ with an unsupported file type.
    Should return 415 or 400 error.
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        files = {
            "doc": ("test.zip", b"dummyzip", "application/zip"),
            "custom_fields": ("fields.txt", b"field1", "text/plain"),
        }
        data = {"user_prompt": "Extract all fields"}
        resp = await ac.post("/document/extract_fields/", files=files, data=data)
        assert resp.status_code in (415, 400)

@pytest.mark.asyncio
@patch("src.app.infrastructure.llm_client.LLMClient.start_session")
async def test_extract_fields_invalid_excel(mock_start_session):
    """
    Test /document/extract_fields/ with invalid Excel file (simulate pandas error).
    Should return 422, 500, or 400 error.
    """
    mock_start_session.side_effect = Exception("Invalid Excel format")
    async with AsyncClient(app=app, base_url="http://test") as ac:
        files = {
            "doc": ("test.xlsx", b"notanexcel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
            "custom_fields": ("fields.txt", b"field1", "text/plain"),
        }
        data = {"user_prompt": "Extract all fields"}
        resp = await ac.post("/document/extract_fields/", files=files, data=data)
        assert resp.status_code in (422, 500, 400)

@pytest.mark.asyncio
@patch("src.app.infrastructure.llm_client.LLMClient.start_session")
async def test_extract_fields_large_file(mock_start_session):
    """
    Test /document/extract_fields/ with a simulated large file error.
    Should return 413 or 400 error.
    """
    mock_start_session.side_effect = Exception("File is too large.")
    async with AsyncClient(app=app, base_url="http://test") as ac:
        files = {
            "doc": ("bigfile.pdf", b"x" * 10_000_000, "application/pdf"),
            "custom_fields": ("fields.txt", b"field1", "text/plain"),
        }
        data = {"user_prompt": "Extract all fields"}
        resp = await ac.post("/document/extract_fields/", files=files, data=data)
        assert resp.status_code in (413, 400)

# --- CHAT ENDPOINT TESTS ---

@pytest.mark.asyncio
@patch("src.app.infrastructure.llm_client.LLMClient.get_chat")
async def test_document_continue_chat_success(mock_get_chat):
    """
    Test /document/continue_chat/ with a valid session_id and prompt.
    Should return 200 and a valid chat response.
    """
    mock_chat = MagicMock()
    mock_chat.send_message.return_value.text = "Hello!"
    mock_get_chat.return_value = mock_chat

    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/document/continue_chat/", data={"session_id": "sid", "prompt": "Hi"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["session_id"] == "sid"
        assert "response" in data

@pytest.mark.asyncio
@patch("src.app.infrastructure.llm_client.LLMClient.get_chat")
async def test_document_continue_chat_invalid_session(mock_get_chat):
    """
    Test /document/continue_chat/ with an invalid session_id.
    Should return 400 or 500 error.
    """
    mock_get_chat.side_effect = Exception("Session not found")
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/document/continue_chat/", data={"session_id": "badid", "prompt": "Hi"})
        assert resp.status_code in (400, 500)