"""
Example 5: Direct API Usage
Shows how to use individual components directly.
"""

from vision.screen_capture import capture_screen, save_screenshot, get_screen_dimensions
from vision.ocr import extract_text, find_text_location
from executor.mouse import click, move_mouse
from executor.keyboard import type_text, press_key

def main():
    print("Example 5: Direct API Usage\n")
    
    # Get screen dimensions
    print("1. Getting screen dimensions...")
    width, height = get_screen_dimensions()
    print(f"✓ Screen size: {width}x{height}")
    
    # Capture screenshot
    print("\n2. Capturing screenshot...")
    screenshot = capture_screen()
    if screenshot is not None:
        print(f"✓ Screenshot captured: {screenshot.shape}")
        save_screenshot(screenshot, 'direct_api_example.png')
    
    # Extract text
    print("\n3. Extracting text with OCR...")
    text = extract_text(screenshot)
    print(f"✓ Extracted {len(text)} characters")
    print(f"  Preview: {text[:100]}..." if len(text) > 100 else f"  Text: {text}")
    
    # Find specific text
    print("\n4. Finding specific text location...")
    # This would find "Start" or other common UI text if present
    coords = find_text_location(screenshot, "Start")
    if coords:
        print(f"✓ Found text at coordinates: {coords}")
    else:
        print("✓ Text not found (this is normal if not visible)")
    
    # Mouse operations
    print("\n5. Testing mouse operations...")
    current_pos = (100, 100)
    print(f"  Moving mouse to {current_pos}...")
    move_mouse(current_pos[0], current_pos[1])
    print(f"✓ Mouse moved")
    
    # Keyboard operations
    print("\n6. Testing keyboard operations...")
    print("  Typing text...")
    type_text("Hello, Screen-Pilot!")
    print("✓ Text typed")
    
    print("\nExample 5: Direct API usage demonstration completed!")

if __name__ == "__main__":
    main()
