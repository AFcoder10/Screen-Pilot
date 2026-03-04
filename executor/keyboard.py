"""
Keyboard control module for Screen-Pilot
"""

import pyautogui
import time
from utils.logger import get_logger
from config.settings import KEYBOARD_DELAY

logger = get_logger()


def type_text(text, interval=None):
    """
    Type text
    
    Args:
        text (str): Text to type
        interval (float): Interval between keystrokes
    """
    try:
        if interval is None:
            interval = KEYBOARD_DELAY
        
        pyautogui.typewrite(text, interval=interval)
        logger.info(f"Typed: {text}")
    except Exception as e:
        logger.error(f"Error typing text: {e}")


def type_text_smart(text):
    """
    Type text using write() for better special character support
    
    Args:
        text (str): Text to type
    """
    try:
        # Use write for better unicode/special char support
        pyautogui.write(text, interval=KEYBOARD_DELAY)
        logger.info(f"Typed (smart): {text}")
    except Exception as e:
        logger.warning(f"Smart type failed, falling back: {e}")
        # Fallback to regular typing
        for char in text:
            pyautogui.press(char)


def press_key(key):
    """
    Press a single key
    
    Args:
        key (str): Key name (e.g., 'enter', 'tab', 'backspace')
    """
    try:
        pyautogui.press(key)
        logger.info(f"Pressed key: {key}")
    except Exception as e:
        logger.error(f"Error pressing key '{key}': {e}")


def press_keys(keys):
    """
    Press multiple keys in sequence
    
    Args:
        keys (list): List of key names
    """
    try:
        for key in keys:
            pyautogui.press(key)
        logger.info(f"Pressed keys: {keys}")
    except Exception as e:
        logger.error(f"Error pressing keys: {e}")


def hotkey(key1, key2, key3=None):
    """
    Press key combination
    
    Args:
        key1 (str): First key (e.g., 'ctrl')
        key2 (str): Second key (e.g., 'c')
        key3 (str): Optional third key
    """
    try:
        if key3:
            pyautogui.hotkey(key1, key2, key3)
            logger.info(f"Hotkey: {key1}+{key2}+{key3}")
        else:
            pyautogui.hotkey(key1, key2)
            logger.info(f"Hotkey: {key1}+{key2}")
    except Exception as e:
        logger.error(f"Error with hotkey: {e}")


def key_down(key):
    """
    Press and hold key
    
    Args:
        key (str): Key name
    """
    try:
        pyautogui.keyDown(key)
        logger.info(f"Key down: {key}")
    except Exception as e:
        logger.error(f"Error with key down: {e}")


def key_up(key):
    """
    Release key
    
    Args:
        key (str): Key name
    """
    try:
        pyautogui.keyUp(key)
        logger.info(f"Key up: {key}")
    except Exception as e:
        logger.error(f"Error with key up: {e}")


def clear_field():
    """Clear current input field"""
    try:
        hotkey('ctrl', 'a')
        time.sleep(0.1)
        press_key('delete')
        logger.info("Cleared input field")
    except Exception as e:
        logger.error(f"Error clearing field: {e}")


def wait(seconds):
    """
    Wait for specified duration
    
    Args:
        seconds (float): Duration in seconds
    """
    try:
        time.sleep(seconds)
        logger.info(f"Waited {seconds} seconds")
    except Exception as e:
        logger.error(f"Error waiting: {e}")
