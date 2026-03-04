"""
Example 4: Complex Workflow
Demonstrates a multi-step workflow combining multiple operations.
"""

from main import ScreenPilot
import time

def main():
    agent = ScreenPilot()
    
    # Example 4: Complex workflow
    print("Example 4: Executing complex multi-step workflow...")
    
    # Step 1: Take initial screenshot
    print("\nStep 1: Capturing current desktop...")
    analysis = agent.capture_and_analyze()
    if analysis:
        print(f"✓ Screen analyzed. Detected {len(analysis['ocr_text'])} characters")
    
    # Step 2: Open application
    print("\nStep 2: Opening applications...")
    agent.run_command("open notepad")
    time.sleep(1)
    
    # Step 3: Perform operations
    print("\nStep 3: Performing actions...")
    agent.run_command("type: This is a test of the Screen-Pilot automation system")
    time.sleep(0.5)
    agent.run_command("press enter")
    agent.run_command("type: It is working correctly!")
    
    # Step 4: Take final screenshot
    print("\nStep 4: Capturing final state...")
    from vision.screen_capture import save_screenshot
    final_analysis = agent.capture_and_analyze()
    if final_analysis:
        save_screenshot(final_analysis['screenshot'], 'workflow_result.png')
        print("✓ Final screenshot saved")
    
    print("\n✓ Complex workflow example completed!")

if __name__ == "__main__":
    main()
