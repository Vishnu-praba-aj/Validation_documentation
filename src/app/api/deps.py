from src.app.application.services.validation_service import ValidationService
from src.app.application.services.document_service import DocumentService

def get_validation_service():
    return ValidationService()

def get_document_service():
    return DocumentService()