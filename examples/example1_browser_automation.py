"""
Example 1: Web Browser Automation
Opens a browser, navigates to GitHub, and searches for a repository.
"""

from main import ScreenPilot

def main():
    agent = ScreenPilot()
    
    # Example 1: Open browser and search
    print("Example 1: Opening browser and searching for Screen-Pilot repo...")
    agent.run_command("open chrome")
    agent.run_command("navigate to github.com")
    agent.run_command("search for screen-pilot")
    agent.run_command("click on screen-pilot repository")
    
    print("✓ Browser automation example completed!")

if __name__ == "__main__":
    main()
