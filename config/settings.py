import os
from dotenv import load_dotenv

load_dotenv()

#LLM-Configuration
GENAI_API_KEY = os.getenv("GENAI_API")
AGENT_DEFINITION_PATH = "config/agent_definitions.yaml"

#Db-Configuration
ORACLE_USER = os.getenv("ORACLE_USER")
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD")
ORACLE_DSN = os.getenv("ORACLE_DSN")
