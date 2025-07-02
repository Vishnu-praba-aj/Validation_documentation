import logging
import time

def setup_logger(log_file="process.log"):
    logger = logging.getLogger("logger")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

        # Console handler
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        # File handler
        fh = logging.FileHandler(log_file)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger

def log_duration(logger, label, start_time):
    duration = time.perf_counter() - start_time
    logger.info(f"{label} took {duration:.3f} seconds")
    return duration