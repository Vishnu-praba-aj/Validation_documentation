import json
from httpx import ASGITransport, AsyncClient
import pytest
from unittest.mock import patch, MagicMock
import pytest_asyncio
from src.app.domain.exception import FileTooLargeError, InvalidFileTypeError
from src.app.api.main import app

@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app, raise_app_exceptions=True)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

# --- VALIDATION ENDPOINT TESTS ---

@pytest.mark.asyncio
@patch("src.app.infrastructure.repo_api_client.RepoApiClient.get_files_from_repo")
@patch("src.app.infrastructure.llm_client.LLMClient.start_session")
async def test_analyze_repo_success(mock_start_session, mock_get_files, async_client):
    mock_get_files.return_value = [{"path": "main.py", "type": ".py", "content": "print(1)"}]
    mock_chat = MagicMock()
    mock_chat.send_message.return_value.text = '{"entities": [{"name": "User", "fields": []}]}'
    mock_start_session.return_value = ("sid", mock_chat)

    resp = await async_client.post("/validation/analyze_repo/", json={"repo_url": "https://github.com/owner/repo"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["session_id"] == "sid"
    assert data["type"] == "validation"
    assert "entities" in data["response"]

@pytest.mark.asyncio
@patch("src.app.infrastructure.repo_api_client.RepoApiClient.get_files_from_repo")
async def test_analyze_repo_invalid_url(mock_get_files, async_client):
    mock_get_files.side_effect = Exception("Invalid repo url")
    resp = await async_client.post("/validation/analyze_repo/", json={"repo_url": "invalid"})
    assert resp.status_code in (400, 500)

@pytest.mark.asyncio
@patch("src.app.infrastructure.repo_api_client.RepoApiClient.get_files_from_repo")
@patch("src.app.infrastructure.llm_client.LLMClient.start_session")
async def test_analyze_repo_llm_malformed_json(mock_start_session, mock_get_files, async_client):
    mock_get_files.return_value = [{"path": "main.py", "type": ".py", "content": "print(1)"}]
    mock_chat = MagicMock()
    mock_chat.send_message.return_value.text = "not a json"
    mock_start_session.return_value = ("sid", mock_chat)

    resp = await async_client.post("/validation/analyze_repo/", json={"repo_url": "https://github.com/owner/repo"})
    assert resp.status_code == 500

# --- DOCUMENT EXTRACTION ENDPOINT TESTS ---

@pytest.mark.asyncio
@patch("src.app.infrastructure.llm_client.LLMClient.start_session")
async def test_extract_fields_success(mock_start_session, async_client):
    mock_chat = MagicMock()
    mock_chat.send_message.return_value.text = json.dumps({
        "session_id": "sid",
        "type": "document_extraction",
        "response": {
            "rows": [{"index": 0, "fields": []}]
        }
    })
    mock_start_session.return_value = ("sid", mock_chat)

    files = {
        "doc": ("test.xlsx", b"dummyexcelbytes", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
        "custom_fields": ("fields.txt", b"field1\nfield2", "text/plain"),
    }
    data = {"user_prompt": "Extract all fields"}

    resp = await async_client.post("/document/extract_fields/", files=files, data=data)
    assert resp.status_code == 200
    data = resp.json()
    assert data["session_id"] == "sid"
    assert data["type"] == "document_extraction"
    assert "rows" in data["response"]

@pytest.mark.asyncio
@patch("src.app.infrastructure.llm_client.LLMClient.start_session")
async def test_extract_fields_unsupported_file_type(mock_start_session, async_client):
    mock_start_session.side_effect = InvalidFileTypeError("Unsupported file type")
    
    files = {
        "doc": ("test.zip", b"dummyzip", "application/zip"),
        "custom_fields": ("fields.txt", b"field1", "text/plain"),
    }
    data = {"user_prompt": "Extract all fields"}

    resp = await async_client.post("/document/extract_fields/", files=files, data=data)
    assert resp.status_code == 415

@pytest.mark.asyncio
@patch("src.app.infrastructure.llm_client.LLMClient.start_session")
async def test_extract_fields_invalid_excel(mock_start_session, async_client):
    mock_start_session.side_effect = Exception("Invalid Excel format")
    files = {
        "doc": ("test.xlsx", b"notanexcel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
        "custom_fields": ("fields.txt", b"field1", "text/plain"),
    }
    data = {"user_prompt": "Extract all fields"}

    resp = await async_client.post("/document/extract_fields/", files=files, data=data)
    assert resp.status_code in (422, 500, 400)

@pytest.mark.asyncio
@patch("src.app.infrastructure.llm_client.LLMClient.start_session")
async def test_extract_fields_large_file(mock_start_session, async_client):
    mock_start_session.side_effect = FileTooLargeError("File is too large.")
    
    files = {
        "doc": ("bigfile.pdf", b"x" * 10_000_000, "application/pdf"),
        "custom_fields": ("fields.txt", b"field1", "text/plain"),
    }
    data = {"user_prompt": "Extract all fields"}

    resp = await async_client.post("/document/extract_fields/", files=files, data=data)
    assert resp.status_code == 413

# --- CHAT ENDPOINT TESTS ---

@pytest.mark.asyncio
@patch("src.app.infrastructure.llm_client.LLMClient.get_chat")
async def test_document_continue_chat_success(mock_get_chat, async_client):
    mock_chat = MagicMock()
    mock_chat.send_message.return_value.text = "Hello!"
    mock_get_chat.return_value = mock_chat

    resp = await async_client.post("/document/continue_chat/", data={"session_id": "sid", "prompt": "Hi"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["session_id"] == "sid"
    assert "response" in data

@pytest.mark.asyncio
@patch("src.app.infrastructure.llm_client.LLMClient.get_chat")
async def test_document_continue_chat_invalid_session(mock_get_chat, async_client):
    mock_get_chat.side_effect = Exception("Session not found")

    resp = await async_client.post("/document/continue_chat/", data={"session_id": "badid", "prompt": "Hi"})
    assert resp.status_code in (400, 500)
