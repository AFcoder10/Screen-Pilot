# Screen-Pilot Architecture

This document describes the system architecture and design decisions for Screen-Pilot.

## System Overview

Screen-Pilot is built on a modular pipeline architecture that processes user commands into executable desktop actions.

```
User Input
    ↓
Command Parser
    ↓
Vision Pipeline
    ├─ Screen Capture
    ├─ OCR Processing
    └─ UI Detection
    ↓
Context Builder
    ├─ UI Analysis
    ├─ Text Recognition
    └─ State Management
    ↓
LLM Planning
    ├─ Gemini API
    ├─ Action Generation
    └─ Validation
    ↓
Execution Engine
    ├─ Mouse Control
    ├─ Keyboard Control
    └─ Action Sequencing
    ↓
Feedback Loop
    ├─ Screen Capture
    ├─ Result Verification
    └─ Error Recovery
```

## Core Modules

### 1. Vision Layer (`vision/`)

**Responsibility**: Extract information from screenshots

#### Components:
- **screen_capture.py**: Screenshot acquisition using MSS
  - Fast screen capture at specified intervals
  - Image preprocessing and resizing
  - Screen dimension detection
  
- **ocr.py**: Text recognition using Tesseract
  - Full page OCR text extraction
  - Regional text detection with bounding boxes
  - Specific text localization for clicking
  
- **ui_detection.py**: UI element detection using YOLO
  - Button and clickable element detection
  - Window boundary detection
  - UI context building

#### Design Decisions:
- MSS chosen for cross-platform, fast screenshot capture
- Tesseract for reliable, free OCR
- YOLO optional for advanced UI detection
- Modular approach allows swapping OCR/detection engines

### 2. LLM Layer (`llm/`)

**Responsibility**: AI reasoning and action generation

#### Components:
- **gemini_client.py**: Gemini API integration
  - Screenshot analysis
  - Action sequence generation
  - Screen understanding
  - Error recovery suggestions

#### Design Decisions:
- Gemini chosen for free tier + vision capabilities
- Base client allows extending other LLM providers
- Image → Base64 conversion for API transmission
- Context-aware prompting for accurate action generation

### 3. Agent Layer (`agent/`)

**Responsibility**: Planning and memory management

#### Components:
- **planner.py**: Action generation and validation
  - Parses LLM output into structured actions
  - Validates action syntax and coordinates
  - Maintains action history
  
- **prompt.py**: System prompts and prompt engineering
  - Core system prompt defining agent behavior
  - Action refinement prompts
  - Context building prompts
  
- **memory.py**: State and context management
  - Screen history tracking
  - Execution context (variables, state)
  - Error logging and recovery

#### Design Decisions:
- Clear action parsing ensures robustness
- Action history enables debugging and learning
- Memory separation (screen vs execution) for modularity
- Deque-based history limits memory usage

### 4. Executor Layer (`executor/`)

**Responsibility**: Desktop control

#### Components:
- **mouse.py**: Mouse control primitives
  - Move, click, scroll, drag operations
  - Position retrieval
  - Failsafe disabled for automation
  
- **keyboard.py**: Keyboard control primitives
  - Text input with special character support
  - Key press operations
  - Hotkey combinations
  - Field clearing

#### Design Decisions:
- PyAutoGUI chosen for cross-platform compatibility
- Separate modules for mouse/keyboard for maintainability
- Generous delays between actions for UI responsiveness
- Type hints for IDE support

### 5. Config Layer (`config/`)

**Responsibility**: Configuration management

#### Components:
- **settings.py**: Centralized settings
  - API keys and model selection
  - Action timing parameters
  - Feature flags
  - Timeout configuration

#### Design Decisions:
- Environment variables for secrets
- Type-safe settings module
- Fallback defaults for optional settings
- Easy to extend for new configuration options

### 6. Utils Layer (`utils/`)

**Responsibility**: Cross-cutting concerns

#### Components:
- **logger.py**: Structured logging
  - File and console output
  - Configurable log levels
  - Timestamp and level information

#### Design Decisions:
- Separate logger module for consistency
- Both file and console logging for development
- Singleton pattern for logger access

## Data Flow

### Command Execution Flow

```
1. User Input
   ├─ Text command
   └─ Voice command (future)

2. Screen Capture
   └─ Screenshot at current time

3. Analysis
   ├─ OCR text extraction
   ├─ UI element detection
   └─ Context building

4. Planning
   ├─ Send to LLM
   ├─ Request action sequence
   └─ Validate outputs

5. Execution
   ├─ Parse action syntax
   ├─ Execute actions in sequence
   ├─ Handle errors gracefully
   └─ Record execution

6. Feedback
   ├─ Optional: Verify completion
   ├─ Optional: Continue if needed
   └─ Log results
```

### Action Format

Actions follow the format:
```
ACTION_NAME(arg1, arg2, ..., argN)
```

Example sequence:
```
MOVE_MOUSE(520, 430)
CLICK(520, 430)
TYPE("screen-pilot")
PRESS("enter")
WAIT(2)
SCREENSHOT()
```

## Memory Management

### Screen Memory
- Maintains deque of recent screenshots
- Stores OCR text from each capture
- Tracks UI context changes
- Max capacity prevents unbounded growth

### Execution Context
- Variables for command state
- Execution state (success/failure)
- Error log for debugging
- Context-specific information

### Agent Memory (Global)
- Screen memory instance
- Execution context instance
- Command history
- Provides unified interface

## Error Handling

### Levels of Error Handling

1. **Action Level**
   - Invalid action syntax
   - Out-of-bounds coordinates
   - Failed mouse clicks

2. **Command Level**
   - Failed action sequences
   - Timeout awaiting UI changes
   - Critical errors

3. **System Level**
   - API connection failures
   - Screenshot capture failure
   - File system errors

### Recovery Strategies

```python
# Retry Logic
for attempt in range(MAX_RETRIES):
    try:
        result = action()
        return result
    except RecoverableError:
        time.sleep(backoff_time)
        
# Fallback
try:
    use_yolo_detection()
except:
    fallback_to_ocr()
```

## Extension Points

### Adding New LLM Models

```python
# In llm/client.py
class OpenAIClient(LLMClient):
    def generate_actions(self, command, context):
        # Implementation specific to OpenAI
        pass
```

### Adding New Vision Engines

```python
# In vision/ocr.py
class EasyOCREngine(OCREngine):
    def extract_text(self, image):
        # EasyOCR implementation
        pass
```

### Adding New Action Types

```python
# In agent/planner.py
VALID_ACTIONS = [
    # Existing actions
    'CUSTOM_ACTION'  # New action
]

# In executor/custom.py
def execute_custom_action(args):
    # Implementation
    pass
```

## Performance Considerations

### Optimization Strategies

1. **Screenshot Optimization**
   - Reduce capture frequency
   - Use lower resolution for initial scan
   - Cache screenshots when possible

2. **OCR Optimization**
   - Only process visible regions
   - Use grayscale conversion
   - Cache OCR results

3. **API Optimization**
   - Batch requests
   - Use vision + text together
   - Implement caching for static content

4. **Action Execution**
   - Minimize delays between actions
   - Parallel processing where safe
   - Early exit on obvious failures

## Security Considerations

### Principles

1. **Isolation**: Actions execute in user's session only
2. **Validation**: Verify all coordinates and inputs
3. **Logging**: Comprehensive audit trail
4. **Failsafe**: No actions on initialization
5. **Consent**: User explicitly triggers automation

### Limitations

- No access to elevated privilege processes
- Cannot bypass OS security restrictions
- Network traffic can be monitored
- API keys must be kept secret

## Testing Strategy

### Test Levels

1. **Unit Tests**: Individual module functions
2. **Integration Tests**: Module interactions
3. **System Tests**: End-to-end workflows
4. **Performance Tests**: Speed and resource usage

### Test Tools

```python
pytest              # Test runner
pytest-cov         # Coverage
pytest-mock        # Mocking
responses          # HTTP mocking
```

## Future Architecture Improvements

### Planned Enhancements

1. **Caching Layer**
   - Cache detected UI elements
   - Reuse OCR results
   - Reduce API calls

2. **Machine Learning**
   - Learn from user corrections
   - Optimize action sequences
   - Predict next likely actions

3. **Multi-Agent**
   - Parallel task execution
   - Agent coordination
   - Distributed processing

4. **Persistent State**
   - Store learned patterns
   - Session history
   - User preferences

5. **Advanced Control Flow**
   - Loops and conditionals
   - Variable substitution
   - Template actions

## Deployment Considerations

### Development
- Local debugging with logging
- Hot reload of modules
- Quick iteration

### Production
- Optimized package
- Minimal logging
- Error reporting
- Version management

## Monitoring & Observability

### Metrics

- Actions per minute
- Success rate
- Average action duration
- Error rate by type
- API latency

### Logging Levels

```
DEBUG: Detailed execution flow
INFO: Key milestones and status
WARNING: Recoverable issues
ERROR: Failed operations
CRITICAL: System failures
```

---

Last Updated: 2024
For questions: support@screenpilot.dev
