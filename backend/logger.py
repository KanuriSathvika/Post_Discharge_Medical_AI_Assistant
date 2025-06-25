"""
logger.py
---------
Configures a logger for the Post-Discharge Medical AI Assistant system.
Logs are saved to a timestamped file in the 'logs' directory for debugging and audit purposes.
"""

# ---------------------- Log Directory Setup --------------------------- #
# Create logs directory if it doesn't exist
import os  # For directory/file operations
os.makedirs("logs", exist_ok=True)

# ---------------------- Logger Configuration -------------------------- #
# Create a logger instance for the application
import logging  # Python standard logging library
from datetime import datetime  # For timestamping log files

logger = logging.getLogger("post_discharge_ai")
logger.setLevel(logging.INFO)  # Set logging level (INFO, DEBUG, etc.)

# Create a file handler that logs to a file with a timestamp in its name
file_handler = logging.FileHandler(f"logs/session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
formatter = logging.Formatter('%(asctime)s — %(levelname)s — %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger if not already present
if not logger.hasHandlers():
    logger.addHandler(file_handler)

# ---------------------- Logger Utility Function ----------------------- #
def save_logger():
    """
    Save the logger configuration to a file for debugging and tracking issues.
    Writes the logger's creation time, log file path, and handler details to logs/logger_config.txt.
    """
    with open("logs/logger_config.txt", "w") as f:
        f.write(f"Logger created on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Log file: {file_handler.baseFilename}\n")
        f.write("Logger handlers:\n")
        for handler in logger.handlers:
            f.write(f"- {handler}\n")