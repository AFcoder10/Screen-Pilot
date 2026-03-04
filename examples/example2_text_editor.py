"""
Example 2: Text Editor Automation
Opens a text editor, writes content, and saves the file.
"""

from main import ScreenPilot
import time

def main():
    agent = ScreenPilot()
    
    # Example 2: Text editor automation
    print("Example 2: Opening text editor and writing content...")
    agent.run_command("open notepad")
    
    time.sleep(1)  # Wait for application to load
    
    agent.run_command("type the following text: Hello World, Screen-Pilot is awesome!")
    agent.run_command("save file as hello_world.txt")
    
    print("✓ Text editor automation example completed!")

if __name__ == "__main__":
    main()
