import logging
import os

os.makedirs("logs", exist_ok=True)
log_file = os.path.join("logs", "process.log")

def setup_logger(log_file=log_file):

    logger = logging.getLogger("logger")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

        # Console handler
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        # File handler
        fh = logging.FileHandler(log_file, mode='a')  # Append mode
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
