from src.app.infrastructure.db import pool
from src.app.application.services.validation_service import ValidationService
from src.app.application.services.document_service import DocumentService
from src.app.application.services.broker_service import BrokerService
from src.app.infrastructure.db.broker_dao import BrokerDAO

def get_validation_service():
    return ValidationService()

def get_document_service():
    return DocumentService()

def get_broker_service():
    dao = BrokerDAO(pool)
    return BrokerService(dao)