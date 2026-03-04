"""
Agent planner for generating action sequences
"""

import re
from utils.logger import get_logger
from llm.gemini_client import get_gemini_client
from agent.prompt import SYSTEM_PROMPT
from config.settings import MAX_RETRIES

logger = get_logger()


class ActionParser:
    """Parse and validate actions from LLM output"""
    
    VALID_ACTIONS = [
        'MOVE_MOUSE', 'CLICK', 'DOUBLE_CLICK', 'RIGHT_CLICK',
        'TYPE', 'PRESS', 'HOTKEY', 'SCROLL', 'DRAG', 'WAIT'
    ]
    
    @staticmethod
    def parse_action(action_str):
        """
        Parse action string
        
        Args:
            action_str (str): Action string (e.g., "CLICK(100, 200)")
            
        Returns:
            tuple: (action_name, args_dict) or None if invalid
        """
        action_str = action_str.strip()
        
        # Match pattern: ACTION(args)
        match = re.match(r'(\w+)\((.*)\)', action_str)
        if not match:
            return None
        
        action_name = match.group(1).upper()
        args_str = match.group(2)
        
        if action_name not in ActionParser.VALID_ACTIONS:
            return None
        
        try:
            # Parse arguments based on action type
            if action_name in ['MOVE_MOUSE', 'CLICK', 'DOUBLE_CLICK', 'RIGHT_CLICK']:
                # Parse: x, y
                coords = [int(x.strip()) for x in args_str.split(',')]
                if len(coords) != 2:
                    return None
                return (action_name, {'x': coords[0], 'y': coords[1]})
            
            elif action_name == 'TYPE':
                # Parse: "text"
                text = args_str.strip().strip('"\'')
                return (action_name, {'text': text})
            
            elif action_name == 'PRESS':
                # Parse: key
                key = args_str.strip().strip('"\'').lower()
                return (action_name, {'key': key})
            
            elif action_name == 'HOTKEY':
                # Parse: key1, key2[, key3]
                keys = [k.strip().strip('"\'').lower() for k in args_str.split(',')]
                if len(keys) < 2 or len(keys) > 3:
                    return None
                return (action_name, {'keys': keys})
            
            elif action_name == 'SCROLL':
                # Parse: x, y, direction, amount
                parts = [p.strip().strip('"\'') for p in args_str.split(',')]
                if len(parts) != 4:
                    return None
                return (action_name, {
                    'x': int(parts[0]),
                    'y': int(parts[1]),
                    'direction': parts[2].lower(),
                    'amount': int(parts[3])
                })
            
            elif action_name == 'DRAG':
                # Parse: x1, y1, x2, y2
                coords = [int(x.strip()) for x in args_str.split(',')]
                if len(coords) != 4:
                    return None
                return (action_name, {
                    'x1': coords[0],
                    'y1': coords[1],
                    'x2': coords[2],
                    'y2': coords[3]
                })
            
            elif action_name == 'WAIT':
                # Parse: seconds
                seconds = float(args_str.strip())
                return (action_name, {'seconds': seconds})
        
        except (ValueError, IndexError) as e:
            logger.warning(f"Could not parse action {action_str}: {e}")
            return None
        
        return None
    
    @staticmethod
    def validate_coordinates(x, y, max_x=1920, max_y=1080):
        """Validate coordinates are within screen bounds"""
        return 0 <= x <= max_x and 0 <= y <= max_y


class Planner:
    """AI planner for generating action sequences"""
    
    def __init__(self):
        self.client = get_gemini_client()
        self.action_history = []
    
    def plan(self, command, screen_context, ocr_text="", max_retries=MAX_RETRIES):
        """
        Generate action plan for user command
        
        Args:
            command (str): User command
            screen_context (dict): Current screen context
            ocr_text (str): Text extracted from screen
            max_retries (int): Number of retries if parsing fails
            
        Returns:
            list: List of parsed actions
        """
        logger.info(f"Planning for command: {command}")
        
        # Get raw actions from LLM
        raw_actions = self.client.generate_actions(command, screen_context, ocr_text)
        
        if not raw_actions:
            logger.warning("No actions generated")
            return []
        
        # Parse and validate actions
        parsed_actions = []
        for raw_action in raw_actions:
            parsed = ActionParser.parse_action(raw_action)
            if parsed:
                parsed_actions.append(parsed)
            else:
                logger.warning(f"Failed to parse action: {raw_action}")
        
        # Store in history
        self.action_history.append({
            'command': command,
            'actions': parsed_actions,
            'timestamp': __import__('time').time()
        })
        
        logger.info(f"Generated {len(parsed_actions)} valid actions")
        return parsed_actions
    
    def refine_actions(self, actions, feedback=""):
        """
        Refine generated actions based on feedback
        
        Args:
            actions (list): Previously generated actions
            feedback (str): Feedback from execution
            
        Returns:
            list: Refined action list
        """
        logger.info("Refining actions based on feedback")
        # TODO: Implement refinement logic using LLM feedback
        return actions
    
    def get_plan_summary(self):
        """Get summary of action planning history"""
        return {
            'total_plans': len(self.action_history),
            'total_actions': sum(len(p['actions']) for p in self.action_history),
            'recent_plans': self.action_history[-5:] if self.action_history else []
        }


def get_planner():
    """Get or create planner instance"""
    return Planner()
