"""
Screen-Pilot: AI Desktop Automation Agent
Main entry point for the agent
"""

import sys
import time
import argparse
from utils.logger import get_logger
from vision.screen_capture import capture_screen, save_screenshot, get_screen_dimensions
from vision.ocr import extract_text, extract_text_with_boxes
from vision.ui_detection import get_ui_context
from executor.mouse import click, move_mouse, scroll
from executor.keyboard import type_text, press_key, hotkey, wait as keyboard_wait
from executor.direct_actions import execute_direct_action
from agent.planner import get_planner, ActionParser
from agent.memory import get_memory
from llm.gemini_client import get_gemini_client

logger = get_logger()


class ScreenPilot:
    """Main automation agent"""
    
    def __init__(self, auto_mode=False):
        self.planner = get_planner()
        self.memory = get_memory()
        logger.info("Using Gemini API")
        self.llm = get_gemini_client()
        self.auto_mode = auto_mode
        self.running = False
        logger.info("Screen-Pilot initialized")
    
    def capture_and_analyze(self):
        """Capture screen and analyze current state"""
        logger.info("Capturing and analyzing screen...")
        
        # Capture screenshot
        screenshot = capture_screen()
        if screenshot is None:
            logger.error("Failed to capture screenshot")
            return None
        
        # Extract text via OCR
        ocr_text = extract_text(screenshot)
        
        # Get UI context
        ui_context = get_ui_context(screenshot)
        
        # Update memory
        self.memory.screen_memory.record_screen(
            time.time(),
            screenshot.shape,
            ocr_text
        )
        self.memory.screen_memory.update_ui_context(ui_context)
        
        return {
            'screenshot': screenshot,
            'ocr_text': ocr_text,
            'ui_context': ui_context
        }
    
    def execute_action(self, action):
        """Execute a single action"""
        action_name, args = action
        
        logger.info(f"Executing: {action_name} with args {args}")
        
        try:
            if action_name == 'MOVE_MOUSE':
                move_mouse(args['x'], args['y'])
            
            elif action_name == 'CLICK':
                click(args['x'], args['y'])
            
            elif action_name == 'DOUBLE_CLICK':
                click(args['x'], args['y'], clicks=2)
            
            elif action_name == 'RIGHT_CLICK':
                click(args['x'], args['y'], button='right')
            
            elif action_name == 'TYPE':
                type_text(args['text'])
            
            elif action_name == 'PRESS':
                press_key(args['key'])
            
            elif action_name == 'HOTKEY':
                keys = args['keys']
                if len(keys) == 2:
                    hotkey(keys[0], keys[1])
                elif len(keys) == 3:
                    hotkey(keys[0], keys[1], keys[2])
            
            elif action_name == 'SCROLL':
                scroll(args['x'], args['y'], args['direction'], args['amount'])
            
            elif action_name == 'WAIT':
                keyboard_wait(args['seconds'])
            
            # Record action
            self.memory.screen_memory.record_action(action, time.time(), "success")
            
            return True
        
        except Exception as e:
            logger.error(f"Error executing action: {e}")
            self.memory.screen_memory.record_action(action, time.time(), f"error: {e}")
            self.memory.execution_context.record_error(f"Failed to execute {action_name}: {e}")
            return False
    
    def execute_plan(self, actions):
        """Execute action sequence with feedback loop"""
        logger.info(f"Executing plan with {len(actions)} actions")
        
        for i, action in enumerate(actions):
            logger.info(f"Action {i+1}/{len(actions)}: {action[0]}")
            
            # Execute action
            success = self.execute_action(action)
            
            if not success and self.auto_mode:
                logger.warning(f"Action failed, skipping remaining actions")
                break
            
            # Small delay between actions
            time.sleep(0.3)
            
            # Optional: Check screen state after each action
            if (i + 1) % 5 == 0 or (i + 1) == len(actions):
                time.sleep(1)  # Wait for UI to settle
        
        logger.info("Plan execution completed")
    
    def run_command(self, command):
        """Execute a user command"""
        logger.info(f"Processing command: {command}")
        self.memory.record_command(command)
        
        # Try direct actions first (for common commands like "open notepad")
        logger.info("Attempting direct action handler...")
        result = execute_direct_action(command)
        if result:
            logger.info("✓ Command executed via direct action handler")
            return True
        
        logger.info("No direct action match, using LLM planner...")
        
        # Capture current state
        analysis = self.capture_and_analyze()
        if not analysis:
            logger.error("Failed to analyze screen")
            return False
        
        # Generate action plan
        actions = self.planner.plan(
            command,
            analysis['ui_context'],
            analysis['ocr_text']
        )
        
        if not actions:
            logger.warning("No actions generated")
            return False
        
        # Execute plan
        self.execute_plan(actions)
        
        return True
    
    def interactive_mode(self):
        """Interactive command mode"""
        logger.info("Entering interactive mode. Type commands (or 'exit' to quit)")
        
        self.running = True
        while self.running:
            try:
                command = input("\n> Screen-Pilot: ").strip()
                
                if not command:
                    continue
                
                if command.lower() in ['exit', 'quit', 'q']:
                    logger.info("Exiting Screen-Pilot")
                    self.running = False
                    break
                
                if command.lower() == 'status':
                    print(self.memory.get_full_context())
                    continue
                
                if command.lower() == 'screenshot':
                    analysis = self.capture_and_analyze()
                    if analysis:
                        save_screenshot(analysis['screenshot'], 'last_screenshot.png')
                        print(f"OCR Text:\n{analysis['ocr_text']}")
                    continue
                
                # Execute command
                self.run_command(command)
            
            except KeyboardInterrupt:
                logger.info("Interrupted by user")
                self.running = False
            except Exception as e:
                logger.error(f"Error in interactive mode: {e}")
    
    def batch_mode(self, commands):
        """Execute batch of commands"""
        logger.info(f"Executing {len(commands)} commands in batch mode")
        
        for i, command in enumerate(commands, 1):
            logger.info(f"Command {i}/{len(commands)}: {command}")
            self.run_command(command)
            time.sleep(1)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Screen-Pilot: AI Desktop Automation Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --interactive
  python main.py --command "open youtube"
  python main.py --screenshot
        """
    )
    
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Interactive mode'
    )
    
    parser.add_argument(
        '--command', '-c',
        type=str,
        help='Execute single command'
    )
    
    parser.add_argument(
        '--screenshot', '-s',
        action='store_true',
        help='Capture and analyze screenshot'
    )
    
    parser.add_argument(
        '--batch', '-b',
        type=str,
        nargs='+',
        help='Execute batch of commands'
    )
    
    parser.add_argument(
        '--auto',
        action='store_true',
        help='Auto mode - fail fast on errors'
    )
    
    args = parser.parse_args()
    
    # Initialize agent
    agent = ScreenPilot(auto_mode=args.auto)
    
    # Handle different modes
    if args.screenshot:
        analysis = agent.capture_and_analyze()
        if analysis:
            save_screenshot(analysis['screenshot'], 'screenshot.png')
            print(f"\nScreen Analysis:")
            print(f"OCR Text:\n{analysis['ocr_text']}")
            print(f"\nUI Elements: {len(analysis['ui_context'].get('buttons', []))} buttons")
    
    elif args.command:
        agent.run_command(args.command)
    
    elif args.batch:
        agent.batch_mode(args.batch)
    
    elif args.interactive:
        agent.interactive_mode()
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
