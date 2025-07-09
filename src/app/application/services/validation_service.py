import time
from src.app.infrastructure.llm_client import LLMClient
from src.app.infrastructure.repo_api_client import RepoApiClient
from src.app.domain.exception import InvalidJSONResponseException, RepoProcessingException
from src.app.domain.models import ValidationLLMResponse
from utils.helpers import extract_controller_names, find_htmls_for_controller, parse_json
from utils.logging import setup_logger
from threading import Lock
import asyncio

MAX_CHUNK_SIZE = 1500
logger = setup_logger()

def chunk_text(text, max_chunk_size=MAX_CHUNK_SIZE):
    for i in range(0, len(text), max_chunk_size):
        yield text[i:i + max_chunk_size]

class ValidationService:
    def __init__(self):
        self.llm_client = LLMClient()
        self.repo_client = RepoApiClient()
        self.cancelled_sessions = set()
        self._lock = Lock()

    async def analyze_repo(self, repo_url):
        if self.is_cancelled(repo_url):
            logger.warning(f"Repo analysis cancelled before start: {repo_url}")
            self.clear_cancellation(repo_url)
            raise RepoProcessingException("Analysis cancelled by user")

        files = self.repo_client.get_files_from_repo(repo_url)
        if not files:
            raise RepoProcessingException()

        code_blocks = []
        html_files = {f["path"]: f["content"] for f in files if f["type"] == ".html"}

        start = time.perf_counter()
        for file in files:
            if self.is_cancelled(repo_url):
                logger.warning(f"Repo analysis cancelled during file parsing: {repo_url}")
                self.clear_cancellation(repo_url)
                raise RepoProcessingException("Analysis cancelled by user")

            if file["type"] == ".html":
                continue
            content = file["content"]
            file_block = f"\nFile: {file['path']}\n{content}"

            if file["type"] == ".js":
                controller_names = extract_controller_names(content)
                associated_html = []
                for controller_name in controller_names:
                    matched_html = find_htmls_for_controller(
                        controller_name,
                        html_files.keys(),
                        html_files.get
                    )
                    if matched_html:
                        associated_html.extend(matched_html)
                if associated_html:
                    file_block += f"\nAssociated HTML:\n" + "\n".join(associated_html)

            code_blocks.append(file_block)

        full_code_text = "\n".join(code_blocks)
        chunks = list(chunk_text(full_code_text))

        if self.is_cancelled(repo_url):
            logger.warning(f"Repo analysis cancelled before LLM session: {repo_url}")
            self.clear_cancellation(repo_url)
            raise RepoProcessingException("Analysis cancelled by user")

        session_id, chat = self.llm_client.start_session("ValidationAgent")

        for idx, chunk in enumerate(chunks):
            if self.is_cancelled(repo_url):
                logger.warning(f"Cancelled mid LLM chunking: {repo_url}")
                self.clear_cancellation(repo_url)
                raise RepoProcessingException("Analysis cancelled by user")

            prompt = f"Code Chunk {idx + 1} of {len(chunks)}:\n{chunk}"
            chat.send_message(prompt)

            # ✅ Here's where you can now await
            await asyncio.sleep(0.1)

        end = time.perf_counter()
        logger.info(f"Prompt send took {end-start:.2f} seconds")

        if self.is_cancelled(repo_url):
            logger.warning(f"Repo analysis cancelled before final prompt: {repo_url}")
            self.clear_cancellation(repo_url)
            raise RepoProcessingException("Analysis cancelled by user")

        final_prompt = (
            "You have now received all code and associated HTML files in the previous chunks. "
            "Now, using ALL the code and HTML files provided, extract and document all validation logic as per the instructions."
        )

        start = time.perf_counter()
        response = chat.send_message(final_prompt)
        await asyncio.sleep(0.1) 
        end = time.perf_counter()
        logger.info(f"ValidationAgent response received in {end-start:.2f} seconds")

        parsed = parse_json(response.text)
        if parsed is None:
            raise InvalidJSONResponseException()

        self.clear_cancellation(repo_url)
        return ValidationLLMResponse(session_id=session_id, type="validation", response=parsed)

    def cancel_analysis(self, repo_url: str):
        with self._lock:
            self.cancelled_sessions.add(repo_url)

    def is_cancelled(self, repo_url: str) -> bool:
        with self._lock:
            return repo_url in self.cancelled_sessions

    def clear_cancellation(self, repo_url: str):
        with self._lock:
            self.cancelled_sessions.discard(repo_url)

        
    