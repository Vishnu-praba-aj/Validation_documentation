from unittest.mock import patch, MagicMock
from src.app.application.services.validation_service import ValidationService

@patch("src.app.application.services.validation_service.LLMClient")
@patch("src.app.application.services.validation_service.RepoApiClient")
def test_analyze_repo_success(mock_repo, mock_llm):
    mock_repo.return_value.get_files_from_repo.return_value = [
        {"path": "main.py", "type": ".py", "content": "print(1)"}
    ]
    mock_chat = MagicMock()
    mock_chat.send_message.return_value.text = '{"entities":[]}'
    mock_llm.return_value.start_session.return_value = ("sid", mock_chat)
    service = ValidationService()
    result = service.analyze_repo("dummy_url")
    assert result.session_id == "sid"
    assert result.type == "validation"