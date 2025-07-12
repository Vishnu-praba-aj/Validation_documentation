from fastapi import Request
from src.app.application.services.validation_service import ValidationService
from src.app.application.services.document_service import DocumentService
from src.app.application.services.broker_service import BrokerService
from src.app.infrastructure.db.broker_dao import BrokerDAO

def get_validation_service():
    return ValidationService()

def get_document_service(request:Request):
    dao = BrokerDAO(request.app.state.pool)
    return DocumentService(dao)

def get_broker_service(request:Request):
    dao = BrokerDAO(request.app.state.pool)
    return BrokerService(dao)