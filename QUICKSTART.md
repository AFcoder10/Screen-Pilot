# Quick Start Guide

Get Screen-Pilot up and running in 5 minutes.

## ⚡ Quick Troubleshooting

If you already installed dependencies but something isn't working:

```powershell
# 1. Verify everything is set up correctly
python verify_setup.py

# 2. If Tesseract isn't found, run setup script
python setup_tesseract.py

# 3. Reinstall dependencies
pip install -r requirements.txt --upgrade --force-reinstall
```

---

## 1. Installation (2 minutes)

### Prerequisites
- Python 3.8+
- **Tesseract OCR** (⚠️ REQUIRED - download from [here](https://github.com/UB-Mannheim/tesseract/wiki))
  - Windows: Download the installer and run it
  - macOS: `brew install tesseract`
  - Linux: `sudo apt-get install tesseract-ocr`
- Google Gemini API key (free from [here](https://makersuite.google.com/))

### Install Screen-Pilot

```bash
# Clone the repository
git clone https://github.com/yourusername/Screen-Pilot.git
cd Screen-Pilot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Upgrade pip and install build tools
python -m pip install --upgrade pip setuptools wheel

# Install dependencies
python -m pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Add your Gemini API key to .env
# Edit .env and replace 'your_gemini_api_key_here' with your actual key
```

**⚠️ Important**: After installing requirements, verify Tesseract is installed:
```bash
tesseract --version
```
If not found, install from [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)

## 2. Configuration (1 minute)

Edit `.env` file (created in step 1):

```bash
# .env
GEMINI_API_KEY=your_actual_api_key_here
MOUSE_SPEED=0.5
KEYBOARD_DELAY=0.05
LOG_LEVEL=INFO
ENABLE_VOICE_INPUT=true
ENABLE_UI_DETECTION=true
```

**Get your API key:**
1. Go to https://makersuite.google.com/
2. Click "Create API Key"
3. Copy the key and paste it in `.env`

## 3. First Run (1 minute)

### Take a screenshot
```bash
python main.py --screenshot
```

This will:
- Capture your current screen
- Extract text using OCR
- Save screenshot to `screenshot.png`
- Print detected text and UI elements

### Interactive mode
```bash
python main.py --interactive
```

Then try:
```
> open notepad
> type hello world
> save file
> exit
```

## 4. Usage Examples (1 minute)

### One-off commands
```bash
python main.py -c "open youtube"
python main.py -c "search for python tutorial"
```

### Batch automation
```bash
python main.py -b "open chrome" "navigate to github.com" "search for screen-pilot"
```

### Python scripting
```python
from main import ScreenPilot

agent = ScreenPilot()
agent.run_command("open spotify and play music")
agent.run_command("minimize window")
agent.run_command("take screenshot")
```

## Common Tasks

### Open an application
```bash
python main.py -c "open notepad"
```

### Type in a text field
```bash
python main.py -c "click search box and type pizza recipe"
```

### Navigate web
```bash
python main.py -c "open browser, go to google.com, search for ai automation"
```

### Fill a form
```bash
python main.py -c "click name field, type John Doe, click email field, type john@example.com"
```

### Screenshot analysis
```bash
python main.py --screenshot
```

## Troubleshooting

### Tesseract not found
```
Error: pytesseract.TesseractNotFoundError: tesseract is not installed or it's not in your PATH
```
**Solution**: Tesseract is REQUIRED for Screen-Pilot to work. Install it:
- **Windows**: Download installer from [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki) and run it
- **macOS**: `brew install tesseract`
- **Linux**: `sudo apt-get install tesseract-ocr`

**Windows: After installation, run setup script:**
```powershell
# This will auto-detect and configure Tesseract
python setup_tesseract.py
```

**Or manually configure Windows PATH:**
1. Install Tesseract (usually to `C:\Program Files\Tesseract-OCR`)
2. Run this in PowerShell:
```powershell
# Verify Tesseract is installed
where tesseract  # Should show installation path

# If not found, add to PATH:
$env:PATH += ";C:\Program Files\Tesseract-OCR"
```

**Verify installation:**
```bash
tesseract --version
```

If the above doesn't work, run the verification script:
```powershell
python verify_setup.py
```

### Google package deprecation warning
```
All support for the `google.generativeai` package has ended...
```
**Solution**: Screen-Pilot has already been updated to use the new `google.genai` package. If you still see this warning:
1. Update requirements.txt to latest version
2. Reinstall packages: `pip install -r requirements.txt --upgrade --force-reinstall`

### API key not working
```
Error: GEMINI_API_KEY not set
```
**Solution**:
1. Get free API key from https://makersuite.google.com/
2. Create `.env` file in project root:
   ```
   GEMINI_API_KEY=your_key_here
   ```
3. Restart Screen-Pilot

### YOLO channel error
```
Error: Given groups=1, weight of size ... expected input... to have 3 channels, but got 4 channels
```
**Solution**: Screen-Pilot automatically handles this now. If you still see it:
1. Update to latest version
2. Reinstall: `pip install -r requirements.txt --upgrade`

### Actions not executing
**Check these**:
1. Coordinates are within screen bounds
2. Application windows are visible
3. Add `WAIT(1)` between actions
4. Check logs in `logs/screen_pilot.log`
5. Verify Tesseract is working: `tesseract --version`

## Next Steps

1. **Read the Full Documentation**: See [README.md](README.md)
2. **Understand Architecture**: See [ARCHITECTURE.md](ARCHITECTURE.md)
3. **Advanced Usage**: See `examples/` folder
4. **Contribute**: See [CONTRIBUTING.md](CONTRIBUTING.md)

## Example Projects

### Browser Automation
```bash
python main.py -c "open browser, navigate to github.com, search for screen-pilot"
```

### Data Entry
```bash
python main.py \
  -b \
  "open spreadsheet" \
  "click cell A1" \
  "type 100" \
  "press enter" \
  "type 200" \
  "save file"
```

### Screenshot Testing
```bash
python main.py -c "open application, take screenshot, verify ui"
```

## Pro Tips

1. **Add waits between actions**: Use `WAIT(1)` for UI to load
2. **Start with screenshots**: Always run `--screenshot` first to see available elements
3. **Use short commands**: Simpler commands = better AI understanding
4. **Check logs**: Always look at `logs/screen_pilot.log` if something fails
5. **Batch mode**: Use batch for complex workflows

## Getting Help

- **Documentation**: [README.md](README.md)
- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **Examples**: See `examples/` folder
- **Issues**: [GitHub Issues](https://github.com/yourusername/Screen-Pilot/issues)
- **Email**: support@screenpilot.dev

## What's Next?

Now that you're up and running:

1. ✅ Read the [README.md](README.md) for comprehensive guide
2. ✅ Check out [examples/](examples/) for sample projects
3. ✅ Explore [ARCHITECTURE.md](ARCHITECTURE.md) for deep dive
4. ✅ Try advanced features in advanced setup guide
5. ✅ Contribute to the project!

Happy automating! 🚀
