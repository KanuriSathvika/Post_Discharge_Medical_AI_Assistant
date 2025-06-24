# logger.py
import logging
from datetime import datetime
import os

# Create logs directory
os.makedirs("logs", exist_ok=True)

# Create logger
logger = logging.getLogger("post_discharge_ai")
logger.setLevel(logging.INFO)

# Create file handler with timestamp
file_handler = logging.FileHandler(f"logs/session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
formatter = logging.Formatter('%(asctime)s — %(levelname)s — %(message)s')
file_handler.setFormatter(formatter)

# Add handler if not already added
if not logger.hasHandlers():
    logger.addHandler(file_handler)
