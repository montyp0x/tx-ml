import os
import logging
from src.config import LOG_FILE

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def setup_logging():
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
