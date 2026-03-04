# Screen-Pilot: AI Desktop Automation Agent

> Autonomous desktop control using AI vision and natural language commands

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Overview

Screen-Pilot is a professional-grade AI desktop automation agent that understands your screen and executes complex tasks through natural language commands. It combines computer vision, OCR, and large language models to intelligently control your desktop.

**🔔 Recent Update**: Screen-Pilot has been updated to use the new `google.genai` package. The deprecated `google-generativeai` package is no longer used. See [QUICKSTART.md](QUICKSTART.md) for setup instructions.

**Use Cases:**
- Automate repetitive desktop tasks
- Test web applications
- Automated data entry
- Screenshot analysis
- Cross-application workflows
- Accessibility automation

## Features

- **🤖 Autonomous Desktop Control**: Execute complex multi-step tasks with natural language
- **👁️ Real-time Screen Understanding**: AI-powered vision analysis of your desktop
- **📝 Natural Language Task Execution**: Simple English commands
- **🧠 AI-driven Task Planning**: Intelligent action sequencing
- **🔄 Feedback Loop**: Continuous screen monitoring and adaptation
- **🎤 Voice Input Support**: Jarvis-like voice command capability (Whisper integration)
- **🎯 Precise UI Detection**: YOLO-powered button and element detection
- **📊 Multi-model Support**: Gemini API with extensible LLM architecture
- **🔐 Cross-platform Automation**: Windows, macOS, Linux support
- **📝 OCR Text Recognition**: Tesseract-powered screen text extraction

## Architecture

```
User Command
    │
    ▼
Voice/Text Input
    │
    ▼
Screen Capture
    │
    ▼
Vision Layer
(OpenCV + OCR)
    │
    ▼
Context Builder
(screen text + UI info)
    │
    ▼
LLM Planner
(AI reasoning)
    │
    ▼
Action Executor
(mouse + keyboard)
    │
    ▼
Feedback Loop
(verify success)
```

## Project Structure

```
Screen-Pilot/
├── agent/                 # AI agent core
│   ├── planner.py        # Action generation and parsing
│   ├── prompt.py         # System prompts
│   └── memory.py         # State and context management
│
├── vision/               # Screen analysis
│   ├── screen_capture.py # Screenshot capture
│   ├── ocr.py           # Text recognition
│   └── ui_detection.py  # Button/element detection
│
├── executor/            # Action execution
│   ├── mouse.py         # Mouse control
│   └── keyboard.py      # Keyboard control
│
├── llm/                 # Language models
│   └── gemini_client.py # Gemini API integration
│
├── config/              # Configuration
│   └── settings.py      # Settings and constants
│
├── utils/               # Utilities
│   └── logger.py        # Logging setup
│
├── main.py              # Entry point
├── requirements.txt     # Dependencies
└── README.md           # This file
```

## Installation

### Prerequisites

- **Python 3.8+**
- **Tesseract OCR**: Install from [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
- **API Key**: Gemini API key from [Google AI Studio](https://makersuite.google.com/)

### Setup

1. **Clone repository**
```bash
git clone https://github.com/yourusername/Screen-Pilot.git
cd Screen-Pilot
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Install Tesseract** (required for OCR)
- **Windows**: Download installer from [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
- **macOS**: `brew install tesseract`
- **Linux**: `sudo apt-get install tesseract-ocr`

5. **Configure API Keys**
```bash
# Create .env file
echo "GEMINI_API_KEY=your_key_here" > .env
```

## Models & APIs

### LLM (Vision & Reasoning)
- **Recommended**: [Google Gemini API](https://makersuite.google.com/)
  - Free tier available
  - Supports vision understanding
  - Low latency

Alternative options:
- GPT-4o (OpenAI)
- Llama 3 (local deployment)

### OCR (Text Recognition)
- **Tesseract**: Free, open-source, reliable
- **EasyOCR**: Alternative with better accuracy

### UI Detection (Advanced)
- **YOLOv8**: Object detection for buttons and UI elements
- Enables precise clicking on detected elements

## Usage

### Interactive Mode
```bash
python main.py --interactive
# or
python main.py -i
```

Then type commands:
```
> open youtube
> search for python tutorials
> play first result
> exit
```

### Single Command
```bash
python main.py --command "open spotify"
python main.py -c "search for music"
```

### Screenshot Analysis
```bash
python main.py --screenshot
python main.py -s
```

### Batch Processing
```bash
python main.py --batch \
  "open browser" \
  "navigate to google.com" \
  "search for screen automation"
```

### Batch Mode
```bash
python main.py -b "command1" "command2" "command3"
```

## Command Examples

```bash
# Web automation
"open youtube and search for python tutorial"
"go to gmail and send email to john@example.com"

# Application control
"open notepad and write hello world"
"minimize all windows"

# System automation
"open settings and change volume to 50 percent"
"take a screenshot and save to desktop"

# Complex workflows
"open chrome, navigate to github, search for screen-pilot, and star the repo"
```

## API Reference

### ScreenPilot Class

```python
from main import ScreenPilot

agent = ScreenPilot(auto_mode=True)

# Execute a command
agent.run_command("open youtube")

# Capture and analyze screen
analysis = agent.capture_and_analyze()
print(analysis['ocr_text'])

# Execute interactive mode
agent.interactive_mode()
```

### Vision Module

```python
from vision.screen_capture import capture_screen, get_screen_dimensions
from vision.ocr import extract_text, find_text_location

# Capture screenshot
screenshot = capture_screen()

# Extract text
text = extract_text(screenshot)

# Find specific text
coords = find_text_location(screenshot, "Search")
```

### Executor Module

```python
from executor.mouse import click, move_mouse, scroll
from executor.keyboard import type_text, press_key, hotkey

# Mouse control
click(500, 300)
move_mouse(100, 200, duration=2)
scroll(500, 300, direction='down', amount=3)

# Keyboard control
type_text("Hello World")
hotkey('ctrl', 'c')
press_key('enter')
```

## Configuration

Edit `config/settings.py` to customize:

```python
# API Configuration
GEMINI_API_KEY = "your_key"
LLM_MODEL = "gemini-pro-vision"

# Screen Configuration
SCREENSHOT_QUALITY = 95
SCREENSHOT_FORMAT = "RGB"

# Action Execution
MOUSE_SPEED = 0.5
KEYBOARD_DELAY = 0.05

# Features
ENABLE_VOICE_INPUT = True
ENABLE_UI_DETECTION = True
ENABLE_FEEDBACK_LOOP = True

# Timeouts
MAX_RETRIES = 3
ACTION_TIMEOUT = 30
UI_LOAD_WAIT = 2
```

## Advanced Features

### Voice Commands (Coming Soon)

```bash
python main.py --voice
# Speak: "Open Youtube"
# Agent listens and executes
```

Requires: `pip install openai-whisper`

### Custom Actions

Extend `executor/` with custom mouse/keyboard patterns:

```python
# In executor/custom.py
def double_tap(key):
    """Double tap a key"""
    press_key(key)
    time.sleep(0.1)
    press_key(key)
```

### UI Element Detection

Use YOLO for robust element detection:

```python
from vision.ui_detection import UIDetector

detector = UIDetector()
buttons = detector.detect_buttons(screenshot)

for button in buttons:
    print(f"Button at ({button['center_x']}, {button['center_y']})")
    click(button['center_x'], button['center_y'])
```

## Troubleshooting

### Tesseract Not Found
```
Error: pytesseract.TesseractNotFoundError
```
**Solution**: Install Tesseract from [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)

### No API Key Provided
```
Error: GEMINI_API_KEY not set
```
**Solution**: Create `.env` file with your API key:
```bash
echo "GEMINI_API_KEY=your_key" > .env
```

### Actions Not Executing
- Check logs in `logs/screen_pilot.log`
- Verify coordinates are within screen bounds
- Ensure UI has time to load (use WAIT action)

### OCR Accuracy Low
- Check image quality in `screenshots/`
- Adjust OCR_CONFIDENCE_THRESHOLD in settings
- Consider using YOLO for UI detection instead

## Performance Tips

1. **Reduce Screenshot Frequency**: Adjust capture intervals
2. **Use UI Detection**: More reliable than text-based clicking
3. **Batch Commands**: Group related actions
4. **Cache Screens**: Reuse screenshot analysis when possible
5. **Optimize Coordinates**: Use OCR to find precise element locations

## Limitations & Considerations

- Requires API access (Gemini, GPT-4o, etc.)
- OCR accuracy depends on text size and quality
- Mouse/keyboard inputs may not work with elevated privilege windows
- Some applications may block automation
- Network-dependent (requires internet for LLM)

## Contributing

Contributions welcome! Areas for improvement:

- [ ] Voice input integration (Whisper)
- [ ] Better error recovery
- [ ] Browser plugin extension
- [ ] Mobile device support
- [ ] Security hardening
- [ ] Performance optimization
- [ ] More vision models support

## Roadmap

- **v1.1**: Voice input with Whisper
- **v1.2**: Web extension for browser automation
- **v1.3**: Mobile device automation
- **v2.0**: Self-improving feedback loops
- **v2.1**: Multi-agent coordination

## License

MIT License - see LICENSE file for details

## Disclaimer

⚠️ **Use responsibly**: This tool can control your computer. Only use in environments you control and trust. Be cautious with automated actions in production systems.

## Support & Contact

- 📧 Email: support@screenpilot.dev
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/Screen-Pilot/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/Screen-Pilot/discussions)

## Acknowledgments

- OpenCV for image processing
- Tesseract for OCR
- Google Gemini for vision-language understanding
- YOLO for object detection

---

**Made with ❤️ for automation enthusiasts**

*Screen-Pilot: Because your time is too valuable for repetitive tasks.*
