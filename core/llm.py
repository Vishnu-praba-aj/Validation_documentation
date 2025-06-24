import google.generativeai as genai
import yaml
from config.settings import GENAI_API_KEY, AGENT_DEFINITION_PATH

genai.configure(api_key=GENAI_API_KEY)

def load_agent_definitions():
    with open(AGENT_DEFINITION_PATH, "r") as f:
        return yaml.safe_load(f)["agents"]

def init_agent_chat(agent_name):
    agents = load_agent_definitions()
    agent = agents[agent_name]
    model = genai.GenerativeModel(agent["model"])
    chat = model.start_chat(history=[])
    chat.send_message(agent["system_prompt"])
    return chat