# Examples Directory

This directory contains practical examples of how to use Screen-Pilot.

## Running Examples

```bash
# Example 1: Web Browser Automation
python example1_browser_automation.py

# Example 2: Text Editor Automation
python example2_text_editor.py

# Example 3: Screenshot Analysis
python example3_screenshot_analysis.py

# Example 4: Complex Multi-step Workflow
python example4_complex_workflow.py

# Example 5: Direct API Usage
python example5_direct_api.py
```

## Examples Overview

### Example 1: Browser Automation
**File**: `example1_browser_automation.py`

Opens a web browser, navigates to GitHub, and searches for repositories.

**Use case**: Web automation, testing, web scraping preparation

### Example 2: Text Editor Automation
**File**: `example2_text_editor.py`

Opens a text editor, types content, and saves a file.

**Use case**: Document creation, data entry, content generation

### Example 3: Screenshot Analysis
**File**: `example3_screenshot_analysis.py`

Captures the current screen and analyzes it using OCR and vision.

**Use case**: Screen inspection, OCR testing, UI analysis

### Example 4: Complex Workflow
**File**: `example4_complex_workflow.py`

Demonstrates a complete multi-step workflow with analysis and file saving.

**Use case**: End-to-end automation tasks, workflow testing

### Example 5: Direct API Usage
**File**: `example5_direct_api.py`

Shows how to use individual Screen-Pilot components directly.

**Use case**: Building custom scripts, understanding the API

## Custom Examples

### Template: Creating Your Own Example

```python
from main import ScreenPilot
from vision.screen_capture import capture_screen, save_screenshot
from executor.mouse import click, move_mouse
from executor.keyboard import type_text, press_key

def main():
    # Initialize agent
    agent = ScreenPilot()
    
    # Your automation logic here
    agent.run_command("your command here")
    
    print("✓ Example completed!")

if __name__ == "__main__":
    main()
```

## Tips for Creating Examples

1. **Start Simple**: Begin with basic operations
2. **Add Delays**: Use `time.sleep()` between operations
3. **Check Logs**: Review `logs/screen_pilot.log` for debugging
4. **Document Purpose**: Include docstring explaining the use case
5. **Handle Errors**: Add try-except blocks for robustness
6. **Verify States**: Use screenshots to verify progress

## Contributing Examples

Found a cool example? Fork and contribute!

1. Create new file: `exampleN_description.py`
2. Add documentation
3. Test thoroughly
4. Submit pull request!

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## Performance Tips

- Use batch mode for multiple commands
- Add strategic waits between actions
- Cache screenshot analysis when possible
- Group related operations

## Troubleshooting Examples

If examples fail:

1. **Check logs**: `cat logs/screen_pilot.log`
2. **Verify API key**: Ensure `.env` has valid Gemini API key
3. **Take screenshot**: Run `python main.py --screenshot` to see screen state
4. **Check coordinates**: Ensure click coordinates are valid
5. **Add delays**: Increase `time.sleep()` values if UI hasn't loaded

## Next Steps

- Read [README.md](../README.md) for comprehensive documentation
- Check [ARCHITECTURE.md](../ARCHITECTURE.md) for system design
- Review [QUICKSTART.md](../QUICKSTART.md) for quick setup guide
