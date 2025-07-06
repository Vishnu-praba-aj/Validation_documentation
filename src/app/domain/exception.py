from fastapi import HTTPException, status

class FileTooLargeError(HTTPException):
    def __init__(self, detail="File is too large."):
        super().__init__(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail=detail)

class SessionNotFoundError(HTTPException):
    def __init__(self, detail="Session not found."):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class InvalidFileTypeError(HTTPException):
    def __init__(self, detail="Invalid or unsupported file type."):
        super().__init__(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail=detail)

class RepoProcessingException(HTTPException):
    def __init__(self, detail="Failed to process repository."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class DocumentProcessingException(HTTPException):
    def __init__(self, detail="Failed to process document."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
