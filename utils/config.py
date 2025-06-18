import os
from dotenv import load_dotenv

load_dotenv()
GENAI_API_KEY = os.getenv("GENAI_API")
LLM_MODEL = "gemini-1.5-flash"
TEMPERATURE = 0