"""
OCR module for reading text from screenshots
"""

import pytesseract
import cv2
import numpy as np
from PIL import Image
import os
import importlib.util
from pathlib import Path
from utils.logger import get_logger
from config.settings import OCR_LANGUAGE, OCR_CONFIDENCE_THRESHOLD

logger = get_logger()

# Try to configure pytesseract path for Windows
try:
    # Check if custom config exists
    config_path = Path("pytesseract_config.py")
    if config_path.exists():
        spec = importlib.util.spec_from_file_location("pytesseract_config", str(config_path))
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        logger.info("Using pytesseract_config for Tesseract path")
except Exception as e:
    logger.debug(f"No custom pytesseract config: {e}")

# Try to auto-detect Tesseract on Windows if not in PATH
try:
    # Check if tesseract is in PATH
    pytesseract.get_tesseract_version()
except Exception as e:
    logger.debug(f"Tesseract not in PATH, trying common locations...")
    
    # Common Windows paths
    common_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    ]
    
    tesseract_found = False
    for path in common_paths:
        if os.path.exists(path):
            pytesseract.pytesseract.pytesseract_cmd = path
            logger.info(f"Found Tesseract at: {path}")
            tesseract_found = True
            break
    
    if not tesseract_found:
        logger.warning(
            "Tesseract not found. Please install it from: "
            "https://github.com/UB-Mannheim/tesseract/wiki"
        )


def extract_text(image):
    """
    Extract text from image using Tesseract OCR
    
    Args:
        image (numpy.ndarray): Input image (BGR or BGRA format)
        
    Returns:
        str: Extracted text
    """
    try:
        # Handle different channel formats
        if len(image.shape) == 3:
            if image.shape[2] == 4:
                # RGBA/BGRA - remove alpha channel
                image = image[:, :, :3]
            
            # Convert BGR to RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Convert to grayscale for better OCR
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) if len(image.shape) == 3 else image
        
        # Apply thresholding
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Extract text
        text = pytesseract.image_to_string(
            thresh,
            lang=OCR_LANGUAGE,
            config='--psm 6'
        )
        
        logger.info(f"OCR extracted {len(text)} characters")
        return text.strip()
    except Exception as e:
        logger.error(f"Error in OCR: {e}")
        return ""


def extract_text_with_boxes(image):
    """
    Extract text with bounding boxes (detailed OCR)
    
    Args:
        image (numpy.ndarray): Input image
        
    Returns:
        list: List of dicts with text and coordinates
    """
    try:
        if len(image.shape) == 3 and image.shape[2] == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Get detailed data
        data = pytesseract.image_to_data(
            thresh,
            lang=OCR_LANGUAGE,
            output_type=pytesseract.Output.DICT,
            config='--psm 6'
        )
        
        results = []
        for i in range(len(data['text'])):
            if float(data['conf'][i]) > OCR_CONFIDENCE_THRESHOLD * 100:
                result = {
                    'text': data['text'][i],
                    'x': data['left'][i],
                    'y': data['top'][i],
                    'width': data['width'][i],
                    'height': data['height'][i],
                    'confidence': float(data['conf'][i]) / 100
                }
                results.append(result)
        
        logger.info(f"Detected {len(results)} text regions")
        return results
    except Exception as e:
        logger.error(f"Error in detailed OCR: {e}")
        return []


def find_text_location(image, target_text):
    """
    Find location of specific text in image
    
    Args:
        image (numpy.ndarray): Input image
        target_text (str): Text to find
        
    Returns:
        tuple: (x, y) center coordinates or None if not found
    """
    try:
        text_boxes = extract_text_with_boxes(image)
        
        for box in text_boxes:
            if target_text.lower() in box['text'].lower():
                center_x = box['x'] + box['width'] // 2
                center_y = box['y'] + box['height'] // 2
                logger.info(f"Found '{target_text}' at ({center_x}, {center_y})")
                return (center_x, center_y)
        
        logger.warning(f"Text '{target_text}' not found")
        return None
    except Exception as e:
        logger.error(f"Error finding text: {e}")
        return None
