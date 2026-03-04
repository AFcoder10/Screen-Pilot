"""
Memory and context management for Screen-Pilot agent
"""

from collections import deque
from utils.logger import get_logger
import json

logger = get_logger()


class ScreenMemory:
    """Manages screen state history and context"""
    
    def __init__(self, max_history=50):
        self.max_history = max_history
        self.screen_history = deque(maxlen=max_history)
        self.ocr_history = deque(maxlen=max_history)
        self.action_history = deque(maxlen=max_history)
        self.ui_context = {}
    
    def record_screen(self, timestamp, image_shape, screen_text=""):
        """
        Record screen state
        
        Args:
            timestamp (float): Unix timestamp
            image_shape (tuple): Image dimensions
            screen_text (str): OCR text
        """
        self.screen_history.append({
            'timestamp': timestamp,
            'shape': image_shape,
            'text_preview': screen_text[:200] if screen_text else ""
        })
        
        if screen_text:
            self.ocr_history.append({
                'timestamp': timestamp,
                'text': screen_text
            })
        
        logger.debug(f"Screen recorded: {image_shape}")
    
    def record_action(self, action, timestamp, result=""):
        """
        Record executed action
        
        Args:
            action (tuple): (action_name, args_dict)
            timestamp (float): Unix timestamp
            result (str): Execution result
        """
        action_name, args = action
        self.action_history.append({
            'name': action_name,
            'args': args,
            'timestamp': timestamp,
            'result': result
        })
        
        logger.debug(f"Action recorded: {action_name}")
    
    def update_ui_context(self, context):
        """
        Update UI context
        
        Args:
            context (dict): UI context information
        """
        self.ui_context = context
        logger.debug(f"UI context updated: {len(context.get('buttons', []))} buttons")
    
    def get_recent_screens(self, count=5):
        """Get recent screen records"""
        return list(self.screen_history)[-count:]
    
    def get_recent_actions(self, count=10):
        """Get recent action records"""
        return list(self.action_history)[-count:]
    
    def get_context_summary(self):
        """Get summary of current context"""
        return {
            'recent_screens': len(self.screen_history),
            'recent_actions': len(self.action_history),
            'ui_buttons': len(self.ui_context.get('buttons', [])),
            'ui_windows': len(self.ui_context.get('windows', []))
        }
    
    def clear_old_entries(self, before_timestamp=None):
        """Clear old history entries"""
        # Deques automatically maintain max length
        logger.info("Memory cleared (automatic via deque max length)")


class ExecutionContext:
    """Manages execution state and variables"""
    
    def __init__(self):
        self.variables = {}
        self.state = {}
        self.errors = []
    
    def set_variable(self, name, value):
        """Set context variable"""
        self.variables[name] = value
        logger.debug(f"Variable set: {name} = {value}")
    
    def get_variable(self, name, default=None):
        """Get context variable"""
        return self.variables.get(name, default)
    
    def update_state(self, key, value):
        """Update execution state"""
        self.state[key] = value
        logger.debug(f"State updated: {key} = {value}")
    
    def get_state(self, key, default=None):
        """Get execution state"""
        return self.state.get(key, default)
    
    def record_error(self, error_msg):
        """Record error"""
        self.errors.append(error_msg)
        logger.warning(f"Error recorded: {error_msg}")
    
    def has_errors(self):
        """Check if there are errors"""
        return len(self.errors) > 0
    
    def get_errors(self):
        """Get all recorded errors"""
        return self.errors.copy()
    
    def clear_errors(self):
        """Clear error log"""
        self.errors.clear()
    
    def get_summary(self):
        """Get context summary"""
        return {
            'variables': len(self.variables),
            'state_keys': len(self.state),
            'errors': len(self.errors),
            'has_errors': self.has_errors()
        }


class AgentMemory:
    """Unified memory management for agent"""
    
    def __init__(self):
        self.screen_memory = ScreenMemory()
        self.execution_context = ExecutionContext()
        self.command_history = deque(maxlen=100)
    
    def record_command(self, command):
        """Record user command"""
        self.command_history.append(command)
        logger.info(f"Command recorded: {command}")
    
    def get_command_history(self, count=10):
        """Get recent commands"""
        return list(self.command_history)[-count:]
    
    def get_full_context(self):
        """Get full agent context"""
        return {
            'screen': self.screen_memory.get_context_summary(),
            'execution': self.execution_context.get_summary(),
            'recent_commands': self.get_command_history(5)
        }


# Global memory instance
_global_memory = None


def get_memory():
    """Get or create global agent memory"""
    global _global_memory
    if _global_memory is None:
        _global_memory = AgentMemory()
    return _global_memory
