from http.client import HTTPException
import time
from src.app.infrastructure.llm_client import LLMClient
from src.app.domain.models import ExtractionLLMResponse
from utils.helpers import parse_json
from utils.logging import setup_logger

logger = setup_logger()

class DocumentService:
    def __init__(self):
        self.llm_client = LLMClient()

    def extract_fields(self, doc_bytes, doc_filename, fields, user_prompt=""):
        try:
            session_id, chat = self.llm_client.start_session(
                "DocumentAgent",
                file_bytes=doc_bytes,
                filename=doc_filename
            )
            field_list = ", ".join(fields)
            prompt = f"""Extract the following fields: {field_list}
{user_prompt.strip() if user_prompt.strip() else ""}
"""
            start = time.perf_counter()
            response = chat.send_message(prompt.strip())
            end = time.perf_counter()
            logger.info(f"DocumentAgent response received in {end - start:.2f} seconds")
            parsed = parse_json(response.text)
            if parsed is None:
                raise HTTPException(status_code=500, detail="LLM response is not valid JSON.")
            return ExtractionLLMResponse(session_id=session_id, type="document_extraction", response=parsed)
        except Exception as e:
            raise e

    def continue_chat(self, session_id, prompt):
        try:
            chat = self.llm_client.get_chat(session_id)
            start = time.perf_counter()
            response = chat.send_message(prompt)
            end = time.perf_counter()
            logger.info(f"DocumentAgent continued chat response received in {end - start:.2f} seconds")
            parsed = parse_json(response.text)
            if parsed is None:
                raise HTTPException(status_code=500, detail="LLM response is not valid JSON.")
            return ExtractionLLMResponse(session_id=session_id, type="document_extraction", response=parsed)
        except Exception as e:
            raise e