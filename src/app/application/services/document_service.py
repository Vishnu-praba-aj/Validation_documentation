import time
from src.app.infrastructure.db.broker_dao import BrokerDAO
from src.app.infrastructure.file_handler import transform_llm_output
from src.app.infrastructure.llm_client import LLMClient
from utils.helpers import parse_json
from utils.logging import setup_logger
from src.app.domain.exception import FileTooLargeException, InvalidFileTypeException, InvalidJSONResponseException, ResourceNotFoundException, UniqueIdExistsException

MAX_FILE_MB = 3
MAX_FILE_SIZE = MAX_FILE_MB * 1024 * 1024

logger = setup_logger()

class DocumentService:
    def __init__(self,dao: BrokerDAO):
        self.llm_client=LLMClient()
        self.dao=dao

    def extract_fields(self, doc_bytes, doc_filename, fields, user_prompt=""):
        if len(doc_bytes) > MAX_FILE_SIZE:
            raise FileTooLargeException()
        if not doc_filename.lower().endswith(('.pdf', '.csv', '.xlsx', '.xls', '.txt')):
            raise InvalidFileTypeException()

        if doc_filename.lower().endswith(('.xlsx', '.xls')):
            doc_type = "excel"
        else:
            doc_type = "pdf/txt"
    
        session_id, chat = self.llm_client.start_session(
            "DocumentAgent",
            file_bytes=doc_bytes,
            filename=doc_filename,
            doc_type=doc_type
        )

        field_list = ", ".join(fields)
        prompt = f"""This document is of type: {doc_type}.
        Extract the following fields: {field_list}
        {user_prompt.strip() if user_prompt.strip() else ""}"""
        
        start = time.perf_counter()
        response = chat.send_message(prompt.strip())
        end = time.perf_counter()
        logger.info(f"DocumentAgent response received in {end - start:.2f} seconds")
        
        parsed = parse_json(response.text)
        if parsed is None:
            raise InvalidJSONResponseException()
        return transform_llm_output(parsed, session_id, doc_type)
    
    def continue_chat(self, session_id: str, prompt: str):
        chat, doc_type = self.llm_client.get_chat(session_id)
        start = time.perf_counter()
        response = chat.send_message(prompt)
        end = time.perf_counter()
        logger.info(f"DocumentAgent continued chat response received in {end - start:.2f} seconds")
        parsed = parse_json(response.text)
        if parsed is None:
            raise InvalidJSONResponseException()
        return transform_llm_output(parsed, session_id, doc_type)
    
    def get_unique_id(self, broker_code:str, unique_id: str, message: str, session_id: str):
        status = self.dao.check_unique_id_exists(broker_code, unique_id)
    
        if status == "BROKER_NOT_FOUND":
            raise ResourceNotFoundException("Broker not found in Broker Reference table")
        elif status == "UNIQUE_ID_EXISTS":
            raise UniqueIdExistsException()
        
        start=time.perf_counter()
        prompt=f"Extract also the field {unique_id}. {message.strip() if message else ''}"
        result=self.continue_chat(session_id, prompt)
        end=time.perf_counter()
        logger.info(f"Chat continuation to extract unique ID completed in {end - start:.2f} seconds")
        return result
