# LLM Provider Setup Guide

Screen-Pilot supports multiple LLM providers. Choose the one that works best for you.

## Supported Providers

### 1. OpenAI GPT-4 (Recommended - Most Reliable)

**Model**: GPT-4o (with vision)

**Setup**:
1. Get API key from https://platform.openai.com/api-keys
2. Edit `.env`:
   ```env
   LLM_PROVIDER=openai
   OPENAI_API_KEY=sk-proj-...
   ```
3. Install package:
   ```bash
   pip install openai
   ```

**Pricing**: Pay-as-you-go (~$0.01-0.03 per request)

---

### 2. Anthropic Claude (High Quality)

**Model**: Claude 3.5 Sonnet (with vision)

**Setup**:
1. Get API key from https://console.anthropic.com/
2. Edit `.env`:
   ```env
   LLM_PROVIDER=anthropic
   ANTHROPIC_API_KEY=sk-ant-...
   ```
3. Install package:
   ```bash
   pip install anthropic
   ```

**Pricing**: Pay-as-you-go (~$0.015 per request)

---

### 3. Ollama (Local - Free & Private)

**Model**: llama3.2-vision or llava

**Setup**:
1. Install Ollama from https://ollama.ai/
2. Pull a vision model:
   ```bash
   ollama pull llama3.2-vision
   ```
3. Start Ollama server:
   ```bash
   ollama serve
   ```
4. Edit `.env`:
   ```env
   LLM_PROVIDER=ollama
   OLLAMA_HOST=http://localhost:11434
   ```

**Pricing**: Free! Runs on your computer

**Requirements**: ~8GB RAM, GPU recommended for faster inference

---

### 4. Google Gemini (Alternative)

**Model**: Gemini Pro Vision

**Setup**:
1. Get API key from https://makersuite.google.com/app/apikey
2. Edit `.env`:
   ```env
   LLM_PROVIDER=gemini
   GEMINI_API_KEY=AIza...
   ```
3. Install package:
   ```bash
   pip install google-genai
   ```

**Pricing**: Free tier available, then pay-as-you-go

---

## Quick Start

### Option 1: OpenAI (Easiest)

```bash
# 1. Install OpenAI
pip install openai

# 2. Copy .env.example to .env
cp .env.example .env

# 3. Edit .env and add:
# LLM_PROVIDER=openai
# OPENAI_API_KEY=your_key_here

# 4. Run Screen-Pilot
python main.py --interactive
```

### Option 2: Local with Ollama (Private & Free)

```bash
# 1. Install Ollama (https://ollama.ai)
# 2. Pull a vision model
ollama pull llama3.2-vision

# 3. Start Ollama (in separate terminal)
ollama serve

# 4. Edit .env:
# LLM_PROVIDER=ollama

# 5. Run Screen-Pilot
python main.py --interactive
```

---

## Comparison

| Provider | Cost | Speed | Quality | Privacy |
|----------|------|-------|---------|---------|
| OpenAI GPT-4o | $$ | Fast | Excellent | Cloud |
| Claude 3.5 | $$ | Fast | Excellent | Cloud |
| Ollama (Local) | Free | Medium | Good | 100% Local |
| Gemini | $/Free | Fast | Good | Cloud |

---

## Troubleshooting

### "API key not valid"
- Double-check your API key in `.env`
- Make sure there are no spaces or quotes around the key
- Verify the key is active on the provider's dashboard

### "Cannot connect to Ollama"
- Make sure Ollama is running: `ollama serve`
- Check the host in `.env` matches your Ollama server
- Try: `curl http://localhost:11434/api/tags`

### "Module not found"
- Install the required package for your provider:
  ```bash
  pip install openai      # For OpenAI
  pip install anthropic   # For Anthropic
  pip install google-genai  # For Gemini
  pip install requests    # For Ollama
  ```

---

## Switching Providers

You can easily switch between providers by changing `LLM_PROVIDER` in `.env`:

```env
# Try OpenAI
LLM_PROVIDER=openai

# Or try Claude
LLM_PROVIDER=anthropic

# Or use local Ollama
LLM_PROVIDER=ollama
```

No code changes needed!
