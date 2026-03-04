"""
Logging utility for Screen-Pilot
"""

import logging
import os
import sys
from config.settings import LOG_LEVEL, LOG_FILE

# Fix Windows console encoding to support UTF-8
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Configure logger
logger = logging.getLogger("ScreenPilot")
logger.setLevel(getattr(logging, LOG_LEVEL))

# File handler with UTF-8 encoding
file_handler = logging.FileHandler(f"logs/{LOG_FILE}", encoding='utf-8')
file_handler.setLevel(getattr(logging, LOG_LEVEL))

# Console handler with UTF-8 encoding
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(getattr(logging, LOG_LEVEL))

# Formatter (using simple checkmarks and crosses)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def get_logger():
    """Get configured logger instance"""
    return logger
