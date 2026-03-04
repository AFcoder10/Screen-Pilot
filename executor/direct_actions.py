"""
Direct action handlers for common commands.
These bypass the LLM and use hardcoded mouse/keyboard actions.
"""
import time
import subprocess
from executor.keyboard import type_text, press_key, hotkey
from utils.logger import get_logger

logger = get_logger()


APP_WINDOW_KEYWORDS = {
    'notepad': ['notepad'],
    'calculator': ['calculator'],
    'calc': ['calculator'],
    'paint': ['paint'],
    'chrome': ['chrome'],
    'edge': ['edge'],
    'firefox': ['firefox'],
    'word': ['word'],
    'excel': ['excel'],
    'powerpoint': ['powerpoint'],
    'code': ['visual studio code', 'vscode'],
    'vs code': ['visual studio code', 'vscode'],
}


APP_PROCESS_NAMES = {
    'notepad': ['notepad.exe'],
    'calculator': ['CalculatorApp.exe', 'calculator.exe'],
    'calc': ['CalculatorApp.exe', 'calculator.exe'],
    'paint': ['mspaint.exe'],
    'chrome': ['chrome.exe'],
    'edge': ['msedge.exe'],
    'firefox': ['firefox.exe'],
    'word': ['WINWORD.EXE'],
    'excel': ['EXCEL.EXE'],
    'powerpoint': ['POWERPNT.EXE'],
    'code': ['Code.exe'],
    'vs code': ['Code.exe'],
}


def open_notepad():
    """Open Notepad using Windows search"""
    logger.info("Opening Notepad...")
    
    try:
        # Press Windows key to open Start menu/search
        logger.info("Step 1: Opening Windows search with Win key...")
        press_key('win')
        time.sleep(1)
        
        # Type 'notepad' to search
        logger.info("Step 2: Typing 'notepad'...")
        type_text("notepad")
        time.sleep(1)
        
        # Press Enter to open notepad
        logger.info("Step 3: Pressing Enter to open...")
        press_key('enter')
        time.sleep(2)
        
        logger.info("✓ Notepad should now be open!")
        return True
        
    except Exception as e:
        logger.error(f"Error opening notepad: {e}")
        import traceback
        traceback.print_exc()
        return False


def open_application(app_name):
    """Generic function to open applications via Windows search"""
    logger.info(f"Opening {app_name}...")
    
    try:
        # Press Windows key to open Start menu/search
        logger.info("Step 1: Opening Windows search with Win key...")
        press_key('win')
        time.sleep(1)
        
        # Type application name
        logger.info(f"Step 2: Typing '{app_name}'...")
        type_text(app_name)
        time.sleep(1)
        
        # Press Enter
        logger.info(f"Step 3: Pressing Enter...")
        press_key('enter')
        time.sleep(2)
        
        logger.info(f"✓ {app_name} should now be open!")
        return True
        
    except Exception as e:
        logger.error(f"Error opening {app_name}: {e}")
        import traceback
        traceback.print_exc()
        return False


def handle_open_command(command):
    """Handle 'open <app>' commands"""
    # Extract app name from command
    words = command.lower().split()
    
    if len(words) >= 2 and words[0] == 'open':
        app_name = ' '.join(words[1:])
        
        # Map common app names
        common_apps = {
            'notepad': open_notepad,
            'calculator': lambda: open_application('calculator'),
            'calc': lambda: open_application('calculator'),
            'paint': lambda: open_application('paint'),
            'word': lambda: open_application('word'),
            'excel': lambda: open_application('excel'),
            'powerpoint': lambda: open_application('powerpoint'),
            'chrome': lambda: open_application('chrome'),
            'firefox': lambda: open_application('firefox'),
            'edge': lambda: open_application('edge'),
            'vs code': lambda: open_application('code'),
            'code': lambda: open_application('code'),
            'spotify': lambda: open_application('spotify'),
            'discord': lambda: open_application('discord'),
            'teams': lambda: open_application('teams'),
            'cmd': lambda: open_application('cmd'),
            'command prompt': lambda: open_application('cmd'),
            'powershell': lambda: open_application('powershell'),
            'terminal': lambda: open_application('terminal'),
        }
        
        # Check if it's a known app
        for app_key, handler in common_apps.items():
            if app_key in app_name:
                return handler()
        
        # Fall back to generic handler
        return open_application(app_name)
    
    return False


def _extract_target_app(command):
    """Extract app name from a close command."""
    command_lower = command.lower().strip()

    if command_lower.startswith('close '):
        target = command_lower[len('close '):].strip()
    else:
        target = command_lower

    if target in ['window', 'app', 'application', 'current window', 'this window', '']:
        return None

    for alias in APP_WINDOW_KEYWORDS:
        if alias in target:
            return alias

    return target


def _close_by_process(app_alias):
    """Close app by process name to avoid affecting other windows."""
    process_names = APP_PROCESS_NAMES.get(app_alias, [])

    for process_name in process_names:
        result = subprocess.run(
            ['taskkill', '/IM', process_name, '/T'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            logger.info(f"Closed {app_alias} via process {process_name}")
            return True

    return False


def _close_by_window_title(app_alias):
    """Close app by window title when process close is unavailable."""
    try:
        import pygetwindow as gw
    except Exception:
        return False

    keywords = APP_WINDOW_KEYWORDS.get(app_alias, [app_alias])

    try:
        all_titles = [title for title in gw.getAllTitles() if title and title.strip()]
        matching_titles = []
        for title in all_titles:
            title_lower = title.lower()
            if any(keyword in title_lower for keyword in keywords):
                matching_titles.append(title)

        if not matching_titles:
            return False

        target_window = gw.getWindowsWithTitle(matching_titles[0])[0]
        if target_window.isMinimized:
            target_window.restore()
        target_window.activate()
        time.sleep(0.3)
        hotkey('alt', 'f4')
        time.sleep(0.8)
        logger.info(f"Closed {app_alias} by window title")
        return True
    except Exception:
        return False


def close_application(command):
    """Close a specific application safely, or close active window if generic."""
    logger.info(f"Closing command received: {command}")

    try:
        target_app = _extract_target_app(command)

        # Generic close command intentionally closes active window
        if target_app is None:
            logger.info("No specific app target detected. Closing active window with Alt+F4...")
            hotkey('alt', 'f4')
            time.sleep(1)
            logger.info("Closed active window")
            return True

        logger.info(f"Target app to close: {target_app}")

        # Prefer process/window targeted close to avoid closing VS Code by mistake
        if _close_by_process(target_app):
            return True

        if _close_by_window_title(target_app):
            return True

        logger.warning(
            f"Could not find '{target_app}' to close. Skipping Alt+F4 to avoid closing the wrong app."
        )
        return False

    except Exception as e:
        logger.error(f"Error closing app from command '{command}': {e}")
        return False


def maximize_window():
    """Maximize current window"""
    logger.info("Maximizing window...")
    try:
        hotkey('win', 'up')
        time.sleep(0.5)
        logger.info("✓ Window maximized!")
        return True
    except Exception as e:
        logger.error(f"Error maximizing: {e}")
        return False


def minimize_window():
    """Minimize current window"""
    logger.info("Minimizing window...")
    try:
        hotkey('win', 'down')
        time.sleep(0.5)
        logger.info("✓ Window minimized!")
        return True
    except Exception as e:
        logger.error(f"Error minimizing: {e}")
        return False


def execute_direct_action(command):
    """Execute direct actions without LLM"""
    command_lower = command.lower()
    
    # Handle compound notepad commands (e.g., "open notepad and write...")
    if 'notepad' in command_lower and ('write' in command_lower or 'type' in command_lower):
        return handle_notepad_with_text(command)
    
    # Handle compound calculator commands (e.g., "open calc and solve...")
    if ('calc' in command_lower or 'calculator' in command_lower) and ('solve' in command_lower or 'calculate' in command_lower or '+' in command or '-' in command or '*' in command or '/' in command):
        return handle_calculator_math(command)
    
    # Handle window management
    if 'maximize' in command_lower or 'maximize window' in command_lower:
        return maximize_window()
    
    if 'minimize' in command_lower or 'minimize window' in command_lower:
        return minimize_window()
    
    if command_lower.startswith('close'):
        return close_application(command)
    
    # Handle simple open commands
    if 'open' in command_lower:
        return handle_open_command(command)
    
    return None


def handle_notepad_with_text(command):
    """Handle 'open notepad and write...' commands"""
    logger.info("Opening Notepad and writing text...")
    
    try:
        # Extract text to write
        text_to_write = ""
        if 'write' in command.lower():
            parts = command.lower().split('write', 1)
            if len(parts) > 1:
                text_to_write = parts[1].strip()
        elif 'type' in command.lower():
            parts = command.lower().split('type', 1)
            if len(parts) > 1:
                text_to_write = parts[1].strip()
        
        # Open notepad first
        logger.info("Step 1: Opening Notepad...")
        press_key('win')
        time.sleep(1)
        type_text("notepad")
        time.sleep(1)
        press_key('enter')
        time.sleep(2)
        
        # Write the text
        if text_to_write:
            logger.info(f"Step 2: Writing text: {text_to_write}")
            type_text(text_to_write)
            logger.info("✓ Text written successfully!")
        else:
            logger.info("✓ Notepad opened (no text to write)")
        
        return True
        
    except Exception as e:
        logger.error(f"Error in notepad command: {e}")
        import traceback
        traceback.print_exc()
        return False


def handle_calculator_math(command):
    """Handle 'open calc and solve X + Y' commands"""
    logger.info("Opening Calculator and performing calculation...")
    
    try:
        # Extract math expression
        math_expr = ""
        if 'solve' in command.lower():
            parts = command.lower().split('solve', 1)
            if len(parts) > 1:
                math_expr = parts[1].strip()
        elif 'calculate' in command.lower():
            parts = command.lower().split('calculate', 1)
            if len(parts) > 1:
                math_expr = parts[1].strip()
        else:
            # Try to find math expression in command
            import re
            match = re.search(r'(\d+\s*[\+\-\*\/]\s*\d+)', command)
            if match:
                math_expr = match.group(1)
        
        # Open calculator
        logger.info("Step 1: Opening Calculator...")
        press_key('win')
        time.sleep(1)
        type_text("calculator")
        time.sleep(1)
        press_key('enter')
        time.sleep(2)
        
        # Type the calculation
        if math_expr:
            logger.info(f"Step 2: Entering calculation: {math_expr}")
            # Clean up the expression for typing
            math_expr = math_expr.replace(' ', '')
            type_text(math_expr)
            time.sleep(0.5)
            press_key('enter')
            logger.info("✓ Calculation entered successfully!")
        else:
            logger.info("✓ Calculator opened (no calculation to perform)")
        
        return True
        
    except Exception as e:
        logger.error(f"Error in calculator command: {e}")
        import traceback
        traceback.print_exc()
        return False
