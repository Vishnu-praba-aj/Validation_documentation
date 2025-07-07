import pytest
from src.app.domain.exception import FileTooLargeError, InvalidFileTypeError, SessionNotFoundError

def test_file_too_large_error():
    with pytest.raises(FileTooLargeError):
        raise FileTooLargeError()

def test_session_not_found_error():
    with pytest.raises(SessionNotFoundError):
        raise SessionNotFoundError()
    
def test_file_too_large_custom_message():
    with pytest.raises(FileTooLargeError) as exc:
        raise FileTooLargeError("Too big!")
    assert "Too big!" in str(exc.value)

def test_invalid_file_type_error():
    with pytest.raises(InvalidFileTypeError):
        raise InvalidFileTypeError()