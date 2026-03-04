"""
Mouse control module for Screen-Pilot
"""

import pyautogui
import time
from utils.logger import get_logger
from config.settings import MOUSE_SPEED
from vision.screen_capture import get_screen_dimensions

logger = get_logger()

# Disable pyautogui's failsafe
pyautogui.FAILSAFE = False


def move_mouse(x, y, duration=None):
    """
    Move mouse to coordinates
    
    Args:
        x (int): X coordinate
        y (int): Y coordinate
        duration (float): Duration of movement in seconds
    """
    try:
        if duration is None:
            duration = MOUSE_SPEED
        
        pyautogui.moveTo(x, y, duration=duration)
        logger.info(f"Mouse moved to ({x}, {y})")
    except Exception as e:
        logger.error(f"Error moving mouse: {e}")


def click(x, y, button='left', clicks=1, interval=0.1):
    """
    Click at coordinates
    
    Args:
        x (int): X coordinate
        y (int): Y coordinate
        button (str): 'left', 'middle', or 'right'
        clicks (int): Number of clicks
        interval (float): Interval between clicks
    """
    try:
        pyautogui.click(x, y, clicks=clicks, button=button, interval=interval)
        logger.info(f"Clicked at ({x}, {y}) with {button} button ({clicks} times)")
    except Exception as e:
        logger.error(f"Error clicking: {e}")


def double_click(x, y):
    """
    Double click at coordinates
    
    Args:
        x (int): X coordinate
        y (int): Y coordinate
    """
    try:
        pyautogui.click(x, y, clicks=2)
        logger.info(f"Double clicked at ({x}, {y})")
    except Exception as e:
        logger.error(f"Error double clicking: {e}")


def right_click(x, y):
    """
    Right click at coordinates
    
    Args:
        x (int): X coordinate
        y (int): Y coordinate
    """
    try:
        pyautogui.click(x, y, button='right')
        logger.info(f"Right clicked at ({x}, {y})")
    except Exception as e:
        logger.error(f"Error right clicking: {e}")


def scroll(x, y, direction='down', amount=3):
    """
    Scroll at coordinates
    
    Args:
        x (int): X coordinate
        y (int): Y coordinate
        direction (str): 'up' or 'down'
        amount (int): Number of scroll units
    """
    try:
        scroll_amount = amount if direction == 'down' else -amount
        pyautogui.scroll(scroll_amount, x, y)
        logger.info(f"Scrolled {direction} at ({x}, {y}) by {amount} units")
    except Exception as e:
        logger.error(f"Error scrolling: {e}")


def drag(x1, y1, x2, y2, duration=0.5):
    """
    Drag from one position to another
    
    Args:
        x1 (int): Start X coordinate
        y1 (int): Start Y coordinate
        x2 (int): End X coordinate
        y2 (int): End Y coordinate
        duration (float): Duration of drag
    """
    try:
        pyautogui.moveTo(x1, y1)
        pyautogui.drag(x2 - x1, y2 - y1, duration=duration)
        logger.info(f"Dragged from ({x1}, {y1}) to ({x2}, {y2})")
    except Exception as e:
        logger.error(f"Error dragging: {e}")


def get_mouse_position():
    """
    Get current mouse position
    
    Returns:
        tuple: (x, y) coordinates
    """
    try:
        x, y = pyautogui.position()
        logger.debug(f"Mouse position: ({x}, {y})")
        return x, y
    except Exception as e:
        logger.error(f"Error getting mouse position: {e}")
        return None, None


def move_to_center():
    """
    Move mouse to center of screen
    """
    try:
        width, height = get_screen_dimensions()
        center_x = width // 2
        center_y = height // 2
        move_mouse(center_x, center_y)
    except Exception as e:
        logger.error(f"Error moving to center: {e}")
