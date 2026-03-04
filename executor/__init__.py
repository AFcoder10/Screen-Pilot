"""Executor module for Screen-Pilot - Action execution"""

from . import mouse, keyboard

# Re-export common functions
from .mouse import (
    click,
    move_mouse,
    double_click,
    right_click,
    scroll,
    drag,
    get_mouse_position,
)

from .keyboard import (
    type_text,
    press_key,
    hotkey,
    key_down,
    key_up,
    clear_field,
    wait,
)

__all__ = [
    'mouse',
    'keyboard',
    'click',
    'move_mouse',
    'double_click',
    'right_click',
    'scroll',
    'drag',
    'get_mouse_position',
    'type_text',
    'press_key',
    'hotkey',
    'key_down',
    'key_up',
    'clear_field',
    'wait',
]
