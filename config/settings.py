import os
from dotenv import load_dotenv

load_dotenv()
GENAI_API_KEY = os.getenv("GENAI_API")
AGENT_DEFINITION_PATH = "config/agent_definitions.yaml"