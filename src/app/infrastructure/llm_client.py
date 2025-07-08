import google.generativeai as genai
import yaml
import uuid
import time
from src.app.domain.exception import SessionNotFoundException
from config.settings import GENAI_API_KEY, AGENT_DEFINITION_PATH
from src.app.infrastructure.file_handler import read_file_as_part
from utils.logging import setup_logger
from .session_manager import session_manager

logger = setup_logger()
genai.configure(api_key=GENAI_API_KEY)

def load_agent_definitions():
    with open(AGENT_DEFINITION_PATH, "r") as f:
        return yaml.safe_load(f)["agents"]

class LLMClient:
    def __init__(self):
        self.agents = load_agent_definitions()

    def start_session(self, agent_name, file_bytes=None, filename=None):
        start = time.perf_counter()
        agent = self.agents[agent_name]
        model = genai.GenerativeModel(
            agent["model"],
            generation_config=genai.types.GenerationConfig(
                temperature=0.0, top_p=1.0, top_k=1
            )
        )
        chat = model.start_chat(history=[])
        session_id = str(uuid.uuid4())
        end = time.perf_counter()
        logger.info(f"{agent_name} and chat initialization took {end-start:.2f} seconds")

        start = time.perf_counter()
        chat.send_message(agent["system_prompt"])
        end = time.perf_counter()
        logger.info(f"System prompt send took {end-start:.2f} seconds")

        if file_bytes and filename:
            start = time.perf_counter()
            file_part = read_file_as_part(file_bytes, filename)
            chat.send_message([file_part])
            end = time.perf_counter()
            logger.info(f"File send took {end-start:.2f} seconds")

        session_manager.add(session_id, chat)
        return session_id, chat

    def get_chat(self, session_id):
        chat = session_manager.get(session_id)
        if not chat:
            raise SessionNotFoundException()
        return chat