"""
Example 3: Screenshot Analysis
Captures current screen and analyzes it using AI vision.
"""

from main import ScreenPilot

def main():
    agent = ScreenPilot()
    
    # Example 3: Screenshot analysis
    print("Example 3: Analyzing current screen...")
    analysis = agent.capture_and_analyze()
    
    if analysis:
        print(f"\nScreen Dimensions: {analysis['screenshot'].shape}")
        print(f"\nOCR Text Detected:\n{analysis['ocr_text'][:200]}...")
        print(f"\nUI Elements Detected: {len(analysis['ui_context'].get('buttons', []))} buttons")
        
        from vision.screen_capture import save_screenshot
        save_screenshot(analysis['screenshot'], 'analyzed_screenshot.png')
        print("\n✓ Screenshot saved to analyzed_screenshot.png")
    else:
        print("✗ Failed to capture or analyze screen")

if __name__ == "__main__":
    main()
