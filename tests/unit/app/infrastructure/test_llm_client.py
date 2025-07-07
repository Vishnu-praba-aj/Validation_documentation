from unittest.mock import patch, MagicMock
from src.app.infrastructure.llm_client import LLMClient

@patch("src.app.infrastructure.llm_client.genai")
def test_start_session_success(mock_genai):
    mock_model = MagicMock()
    mock_chat = MagicMock()
    mock_model.start_chat.return_value = mock_chat
    mock_genai.GenerativeModel.return_value = mock_model

    client = LLMClient()
    session_id, chat = client.start_session("ValidationAgent")
    assert session_id
    assert chat == mock_chat

@patch("src.app.infrastructure.llm_client.genai")
def test_start_session_with_file(mock_genai):
    mock_model = MagicMock()
    mock_chat = MagicMock()
    mock_model.start_chat.return_value = mock_chat
    mock_genai.GenerativeModel.return_value = mock_model

    client = LLMClient()
    session_id, chat = client.start_session("DocumentAgent", file_bytes=b"abc", filename="test.pdf")
    assert session_id
    assert chat == mock_chat

@patch("src.app.infrastructure.llm_client.genai")
def test_llm_malformed_json(mock_genai):
    mock_model = MagicMock()
    mock_chat = MagicMock()
    mock_chat.send_message.return_value.text = "not a json"
    mock_model.start_chat.return_value = mock_chat
    mock_genai.GenerativeModel.return_value = mock_model

    client = LLMClient()
    session_id, chat = client.start_session("ValidationAgent")
    resp = chat.send_message("prompt")
    assert isinstance(resp.text, str)