"""
Configuration settings for Screen-Pilot agent
"""

import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
# Choose your LLM provider: "gemini", "openai", "anthropic", "ollama"
LLM_PROVIDER = "gemini"  # Using Gemini

# API Keys
GEMINI_API_KEY = "AIzaSyBIlPztZw12032F_-TfdZ_IhOeCoD7zjYg"

# Model Configuration
LLM_MODELS = {
    "gemini": "gemini-pro-vision",
    "openai": "gpt-4o",  # gpt-4o has vision capabilities
    "anthropic": "claude-3-5-sonnet-20241022",  # Claude 3.5 Sonnet
    "ollama": "llama3.2-vision",  # Local model
}
LLM_MODEL = LLM_MODELS.get(LLM_PROVIDER, "gpt-4o")

# Ollama Configuration (for local models)
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# Screen Configuration
SCREENSHOT_QUALITY = 95
SCREENSHOT_FORMAT = "RGB"

# OCR Configuration
OCR_LANGUAGE = "eng"
OCR_CONFIDENCE_THRESHOLD = 0.5

# UI Detection Configuration
USE_YOLO = True
YOLO_CONFIDENCE = 0.5

# Action Execution Configuration
MOUSE_SPEED = 0.5
KEYBOARD_DELAY = 0.05

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FILE = "screen_pilot.log"

# Features
ENABLE_VOICE_INPUT = True
ENABLE_UI_DETECTION = True
ENABLE_FEEDBACK_LOOP = True

# Max retries and timeouts
MAX_RETRIES = 3
ACTION_TIMEOUT = 30
UI_LOAD_WAIT = 2
