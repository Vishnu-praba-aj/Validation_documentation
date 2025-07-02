import fitz, pandas as pd
from utils.logging import log_duration, setup_logger
import time

logger = setup_logger()

def extract_text_from_file(path):
    start = time.perf_counter()
    if path.endswith(".pdf"):
        try:
            doc = fitz.open(path)
            text = "".join([page.get_text() for page in doc])
            log_duration(logger, "PDF text extraction", start)  
            return text
        except Exception as e:
            logger.error(f"Failed to extract text from PDF: {e}")
            raise ValueError(f"Failed to extract text from PDF: {e}")

    elif path.endswith(".txt"):
        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
                log_duration(logger, "TXT file read", start) 
                return text
        except Exception as e:
            logger.error(f"Failed to read text file: {e}")
            raise ValueError(f"Failed to read text file: {e}")

    elif path.endswith((".xls", ".xlsx")):
        try:
            text = pd.read_excel(path).to_string(index=False)
            log_duration(logger, "Excel extraction", start) 
            return text
        except Exception as e:
            logger.error(f"Failed to extract from Excel: {e}")
            raise ValueError(f"Failed to extract from Excel: {e}")

    logger.error(f"Unsupported file format: {path}")
    raise Exception(f"Unsupported file format: {path}")
