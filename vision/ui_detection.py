"""
UI Detection module for identifying UI elements on screen
Uses YOLO for object detection of buttons, icons, windows
"""

import cv2
import numpy as np
from utils.logger import get_logger
from config.settings import USE_YOLO, YOLO_CONFIDENCE

logger = get_logger()

# Placeholder for YOLO integration
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    logger.warning("YOLO not installed. UI detection features will be limited.")


class UIDetector:
    """UI element detection using YOLO"""
    
    def __init__(self):
        self.model = None
        if YOLO_AVAILABLE and USE_YOLO:
            try:
                self.model = YOLO("yolov8m.pt")
                logger.info("YOLO model loaded")
            except Exception as e:
                logger.warning(f"Could not load YOLO model: {e}")
    
    def detect_buttons(self, image):
        """
        Detect buttons and clickable elements
        
        Args:
            image (numpy.ndarray): Input image (3-channel RGB/BGR)
            
        Returns:
            list: List of detected buttons with coordinates
        """
        if not YOLO_AVAILABLE or self.model is None:
            logger.warning("YOLO not available for button detection")
            return []
        
        try:
            # Ensure image is 3-channel (RGB/BGR)
            if len(image.shape) == 3 and image.shape[2] == 4:
                # Remove alpha channel if present
                image = image[:, :, :3]
            
            results = self.model(image, conf=YOLO_CONFIDENCE)
            buttons = []
            
            for result in results:
                for box in result.boxes:
                    # Filter for button-like objects
                    x1, y1, x2, y2 = box.xyxy[0]
                    buttons.append({
                        'x1': float(x1),
                        'y1': float(y1),
                        'x2': float(x2),
                        'y2': float(y2),
                        'center_x': float((x1 + x2) / 2),
                        'center_y': float((y1 + y2) / 2),
                        'confidence': float(box.conf[0])
                    })
            
            logger.info(f"Detected {len(buttons)} UI elements")
            return buttons
        except Exception as e:
            logger.error(f"Error detecting UI elements: {e}")
            return []
    
    def detect_windows(self, image):
        """
        Detect window boundaries
        
        Args:
            image (numpy.ndarray): Input image
            
        Returns:
            list: List of detected windows
        """
        # Use edge detection as fallback
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            windows = []
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                # Filter by size (skip too small or too large)
                if 50 < w < 1800 and 50 < h < 1000:
                    windows.append({
                        'x': x,
                        'y': y,
                        'width': w,
                        'height': h
                    })
            
            logger.info(f"Detected {len(windows)} windows")
            return windows
        except Exception as e:
            logger.error(f"Error detecting windows: {e}")
            return []


def get_ui_context(image):
    """
    Get comprehensive UI context from image
    
    Args:
        image (numpy.ndarray): Input image
        
    Returns:
        dict: UI context information
    """
    try:
        detector = UIDetector()
        
        context = {
            'buttons': detector.detect_buttons(image),
            'windows': detector.detect_windows(image),
            'image_shape': image.shape,
        }
        
        logger.info(f"UI context generated: {len(context['buttons'])} buttons, {len(context['windows'])} windows")
        return context
    except Exception as e:
        logger.error(f"Error getting UI context: {e}")
        return {'buttons': [], 'windows': []}
