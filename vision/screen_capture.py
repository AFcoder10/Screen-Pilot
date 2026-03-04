"""
Screen capture module for Screen-Pilot
"""

import mss
import numpy as np
from PIL import Image
import cv2
from utils.logger import get_logger

logger = get_logger()


def capture_screen(monitor_index=1):
    """
    Capture screenshot from screen
    
    Args:
        monitor_index (int): Monitor index to capture (1 = primary)
        
    Returns:
        numpy.ndarray: Screenshot as numpy array (RGB format)
    """
    try:
        with mss.mss() as sct:
            monitor = sct.monitors[monitor_index]
            screenshot = np.array(sct.grab(monitor))
            
            # Convert RGBA to RGB if needed (remove alpha channel)
            if len(screenshot.shape) == 3 and screenshot.shape[2] == 4:
                screenshot = screenshot[:, :, :3]
                # MSS captures in BGRA, convert to BGR for OpenCV
                screenshot = screenshot[:, :, ::-1]
            
            logger.info(f"Screenshot captured: {screenshot.shape}")
            return screenshot
    except Exception as e:
        logger.error(f"Error capturing screenshot: {e}")
        return None


def save_screenshot(image, filename="screenshot.png"):
    """
    Save screenshot to file
    
    Args:
        image (numpy.ndarray): Image array
        filename (str): Output filename
    """
    try:
        img = Image.fromarray(image)
        img.save(filename)
        logger.info(f"Screenshot saved to {filename}")
    except Exception as e:
        logger.error(f"Error saving screenshot: {e}")


def resize_image(image, scale=0.5):
    """
    Resize image for faster processing
    
    Args:
        image (numpy.ndarray): Input image
        scale (float): Scale factor
        
    Returns:
        numpy.ndarray: Resized image
    """
    try:
        height, width = image.shape[:2]
        new_width = int(width * scale)
        new_height = int(height * scale)
        resized = cv2.resize(image, (new_width, new_height))
        return resized
    except Exception as e:
        logger.error(f"Error resizing image: {e}")
        return image


def get_screen_dimensions():
    """
    Get screen dimensions
    
    Returns:
        tuple: (width, height) of primary monitor
    """
    try:
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            width = monitor["width"]
            height = monitor["height"]
            logger.info(f"Screen dimensions: {width}x{height}")
            return width, height
    except Exception as e:
        logger.error(f"Error getting screen dimensions: {e}")
        return 1920, 1080  # Default fallback
