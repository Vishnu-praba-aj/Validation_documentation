from unittest.mock import patch, MagicMock
from src.app.application.services.document_service import DocumentService

@patch("src.app.application.services.document_service.LLMClient")
def test_extract_fields_success(mock_llm):
    mock_chat = MagicMock()
    mock_chat.send_message.return_value.text = '{"response": {"rows": []}}'
    mock_llm.return_value.start_session.return_value = ("sid", mock_chat)
    service = DocumentService()
    result = service.extract_fields(b"abc", "test.pdf", ["field1"], "")
    assert result.session_id == "sid"
    assert result.type == "document_extraction"