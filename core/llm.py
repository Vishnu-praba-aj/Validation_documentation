import google.generativeai as genai
import yaml
from config.settings import GENAI_API_KEY, AGENT_DEFINITION_PATH
from utils.logging import log_duration, setup_logger  
import time

logger = setup_logger()

genai.configure(api_key=GENAI_API_KEY)

def load_agent_definitions():
    with open(AGENT_DEFINITION_PATH, "r") as f:
        return yaml.safe_load(f)["agents"]

def init_agent_chat(agent_name):
    start = time.perf_counter()
    agents = load_agent_definitions()
    agent = agents[agent_name]
    model = genai.GenerativeModel(
        agent["model"],
        generation_config=genai.types.GenerationConfig(
            temperature=0.0, 
            top_p=1.0,
            top_k=1
        )
    )
    chat = model.start_chat(history=[])
    log_duration(logger, f"{agent_name} and chat initialization", start)
    start = time.perf_counter()
    chat.send_message(agent["system_prompt"])
    log_duration(logger, "System prompt send", start)
    return chat