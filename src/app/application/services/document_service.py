import time
from src.app.infrastructure.llm_client import LLMClient
from src.app.domain.models import ExtractionLLMResponse
from utils.helpers import parse_json
from utils.logging import setup_logger
from src.app.domain.exception import FileTooLargeException, InvalidFileTypeException, InvalidJSONResponseException
import asyncio
import json

MAX_FILE_MB = 3
MAX_FILE_SIZE = MAX_FILE_MB * 1024 * 1024

logger = setup_logger()

class DocumentService:
    def __init__(self):
        self.llm_client = LLMClient()
        self.active_tasks = {}
        

    async def extract_fields(self, doc_bytes, doc_filename, fields, user_prompt="", client_session_id=None):
        if len(doc_bytes) > MAX_FILE_SIZE:
            raise FileTooLargeException()
        if not doc_filename.lower().endswith(('.pdf', '.csv', '.xlsx', '.xls', '.txt')):
            raise InvalidFileTypeException()

        session_id, chat = self.llm_client.start_session(
            "DocumentAgent",
            file_bytes=doc_bytes,
            filename=doc_filename,
            session_id=client_session_id
        )

        # If no client-provided session ID, fall back to server one
        effective_session_id = client_session_id or session_id
        if client_session_id:
            self.llm_client.session_mapping[client_session_id] = session_id

        field_list = ", ".join(fields)
        prompt = f"""Extract the following fields: {field_list}
    {user_prompt.strip() if user_prompt.strip() else ""}
    """

        async def run_extraction():
            try:
                start = time.perf_counter()
                response = await asyncio.to_thread(chat.send_message, prompt.strip())
                end = time.perf_counter()
                logger.info(f"DocumentAgent response received in {end - start:.2f} seconds")
                parsed = parse_json(response.text)
                if parsed is None:
                    raise InvalidJSONResponseException()
                return ExtractionLLMResponse(session_id=effective_session_id, type="document_extraction", response=parsed)
            finally:
                self.active_tasks.pop(effective_session_id, None)  # Clean up using effective ID

        task = asyncio.create_task(run_extraction())
        logger.info(f"Storing task for session_id: {effective_session_id}")
        self.active_tasks[effective_session_id] = task
        return await task


        
    async def continue_chat(self, session_id, prompt):
        actual_session_id = self.llm_client.session_mapping.get(session_id, session_id)
        chat = self.llm_client.get_chat(actual_session_id)
        start = time.perf_counter()
        response = chat.send_message(prompt)
        end = time.perf_counter()
        logger.info(f"DocumentAgent continued chat response received in {end - start:.2f} seconds")
       
        parsed = parse_json(response.text)
        if parsed is None:
            raise InvalidJSONResponseException()
        return ExtractionLLMResponse(session_id=session_id, type="document_extraction", response=parsed)
        
    async def cancel_analysis(self, session_id: str):
        effective_id = self.llm_client.session_mapping.get(session_id, session_id)

       
        for _ in range(5):
            task = self.active_tasks.get(effective_id)
            if task:
                break
            await asyncio.sleep(0.1)

        task = self.active_tasks.get(effective_id)
        if task and not task.done():
            task.cancel()
            logger.info(f"Cancelled analysis for session_id: {effective_id}")
        else:
            logger.info(f"No active task to cancel for session_id: {effective_id}")

