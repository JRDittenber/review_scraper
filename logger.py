# logger.py
import logging

def setup_logger():
    logger = logging.getLogger("app_logger")
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler("app.log")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger
