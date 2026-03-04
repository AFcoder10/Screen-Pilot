"""
Gemini LLM client for Screen-Pilot
Migrated from deprecated google.generativeai to google.genai
"""

import base64
import json
import io
from PIL import Image

try:
    import google.genai as genai
except ImportError:
    # Fallback for older installations
    import google.generativeai as genai
    
from utils.logger import get_logger
from config.settings import GEMINI_API_KEY, LLM_MODEL

logger = get_logger()

# Configure API - Try different approaches
try:
    if GEMINI_API_KEY and hasattr(genai, 'configure'):
        genai.configure(api_key=GEMINI_API_KEY)
        logger.info("✓ Gemini API configured successfully")
except AttributeError:
    logger.info("Using alternative Gemini configuration method")
except Exception as e:
    logger.warning(f"Warning during Gemini configuration: {e}")


class GeminiClient:
    """Gemini API client for vision and reasoning tasks"""
    
    def __init__(self, model_name=None):
        self.model_name = model_name or LLM_MODEL or "gemini-pro-vision"
        self.api_key = GEMINI_API_KEY
        self.model = None

        if not self.api_key:
            logger.error("GEMINI_API_KEY not set. Please add it to .env")
            return
        
        try:
            # Configure with API key
            if hasattr(genai, 'configure'):
                genai.configure(api_key=self.api_key)
            
            # Create model
            self.model = genai.GenerativeModel(self.model_name)
            logger.info(f"✓ Gemini client initialized with model: {self.model_name}")
        except Exception as e:
            logger.error(f"✗ Error initializing Gemini: {e}")
            self.model = None
    
    def image_to_base64(self, image):
        """
        Convert numpy array to base64
        
        Args:
            image (numpy.ndarray): Image array
            
        Returns:
            str: Base64 encoded image
        """
        try:
            img = Image.fromarray(image)
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            return img_str
        except Exception as e:
            logger.error(f"Error converting image to base64: {e}")
            return None
    
    def analyze_screenshot(self, image, ocr_text=""):
        """
        Analyze screenshot and extract UI information
        
        Args:
            image (numpy.ndarray): Screenshot image
            ocr_text (str): OCR extracted text
            
        Returns:
            str: Analysis result
        """
        if not self.model:
            logger.error("Gemini model not initialized")
            return ""
        
        try:
            # Prepare image
            img_base64 = self.image_to_base64(image)
            if not img_base64:
                return ""
            
            # Create prompt
            prompt = f"""Analyze this screenshot and provide a concise description:
1. What application is open?
2. List visible UI elements (buttons, inputs, windows)
3. What is the current state/context?
4. Coordinates of important clickable elements if visible

OCR Text Found:
{ocr_text}

Respond in JSON format with keys: app, elements, state, coordinates"""
            
            # Get response
            response = self.model.generate_content([
                {"mime_type": "image/png", "data": img_base64},
                prompt
            ])
            
            logger.info("Screenshot analysis completed")
            return response.text
        except Exception as e:
            logger.error(f"Error analyzing screenshot: {e}")
            return ""
    
    def generate_actions(self, command, screen_context, ocr_text=""):
        """
        Generate action sequence from user command
        
        Args:
            command (str): User command (e.g., "open youtube")
            screen_context (dict): Current screen context
            ocr_text (str): OCR extracted text
            
        Returns:
            list: List of action strings
        """
        if not self.model:
            logger.error("Gemini model not initialized")
            return []
        
        try:
            prompt = f"""You are a desktop automation agent. 
Given the user command and current screen state, generate ONLY valid action commands.

User Command: {command}

Current Screen Context:
{json.dumps(screen_context)}

OCR Text on Screen:
{ocr_text}

Available Actions:
- MOVE_MOUSE(x, y)
- CLICK(x, y)
- DOUBLE_CLICK(x, y)
- RIGHT_CLICK(x, y)
- TYPE(text)
- PRESS(key)
- HOTKEY(key1, key2)
- SCROLL(x, y, direction, amount)
- DRAG(x1, y1, x2, y2)
- WAIT(seconds)

Rules:
1. Output ONLY actions, one per line
2. Be precise with coordinates
3. Use actual coordinates from screen context
4. Do not explain or add comments
5. If text contains quotes, escape them
6. For special keys use: enter, tab, escape, backspace, delete, etc.

Generate action sequence:"""
            
            response = self.model.generate_content(prompt)
            
            # Parse response
            actions = [line.strip() for line in response.text.split('\n') if line.strip()]
            logger.info(f"Generated {len(actions)} actions")
            return actions
        except Exception as e:
            logger.error(f"Error generating actions: {e}")
            return []
    
    def understand_screen(self, image, ocr_text=""):
        """
        Get natural language understanding of screen
        
        Args:
            image (numpy.ndarray): Screenshot
            ocr_text (str): OCR text
            
        Returns:
            str: Understanding of what's on screen
        """
        if not self.model:
            logger.error("Gemini model not initialized")
            return ""
        
        try:
            img_base64 = self.image_to_base64(image)
            if not img_base64:
                return ""
            
            prompt = f"""Briefly describe what you see on this screen in 2-3 sentences.
Focus on the main application and user-actionable elements.

Detected text:
{ocr_text}"""
            
            response = self.model.generate_content([
                {"mime_type": "image/png", "data": img_base64},
                prompt
            ])
            
            return response.text
        except Exception as e:
            logger.error(f"Error understanding screen: {e}")
            return ""


def get_gemini_client():
    """Get or create Gemini client"""
    return GeminiClient()
