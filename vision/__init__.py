"""Vision module for Screen-Pilot - Screen analysis and UI detection"""

from .screen_capture import (
    capture_screen,
    save_screenshot,
    resize_image,
    get_screen_dimensions
)
from .ocr import extract_text, extract_text_with_boxes, find_text_location
from .ui_detection import UIDetector, get_ui_context

__all__ = [
    'capture_screen',
    'save_screenshot',
    'resize_image',
    'get_screen_dimensions',
    'extract_text',
    'extract_text_with_boxes',
    'find_text_location',
    'UIDetector',
    'get_ui_context',
]
