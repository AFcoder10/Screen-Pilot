# Contributing to Screen-Pilot

Thank you for considering contributing to Screen-Pilot! We welcome contributions from everyone, whether it's bug reports, feature requests, documentation improvements, or code contributions.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/Screen-Pilot.git
   cd Screen-Pilot
   ```
3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
4. **Install development dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov black flake8 mypy
   ```

## Development Workflow

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and follow the code style:
   - Use [Black](https://github.com/psf/black) for formatting
   - Follow PEP 8 naming conventions
   - Add type hints where possible
   - Write docstrings for all functions

3. **Run tests** before committing:
   ```bash
   pytest
   pytest --cov=. --cov-report=html  # Coverage report
   ```

4. **Check code quality**:
   ```bash
   black .
   flake8 .
   mypy .
   ```

5. **Commit with clear messages**:
   ```bash
   git commit -m "feat: Add feature X"
   git commit -m "fix: Resolve issue with Y"
   git commit -m "docs: Improve README"
   git commit -m "refactor: Optimize performance in module Z"
   ```

6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request** on GitHub with:
   - Clear title and description
   - Reference to related issues
   - Screenshots/examples if applicable

## Code Style

### Python Style
```python
"""Module docstring explaining purpose"""

from typing import Optional, List, Dict

def function_name(param1: str, param2: int) -> Optional[Dict]:
    """
    Brief description of function.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
    """
    pass
```

### Commit Message Format
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style/formatting
- `refactor:` Code restructuring
- `perf:` Performance improvements
- `test:` Test additions/changes
- `chore:` Build/config/dependency changes

Example: `feat: Add voice command support with Whisper`

## Testing

### Writing Tests
```python
# In tests/test_module.py
import pytest
from module import function

def test_function_basic():
    result = function("input")
    assert result == "expected"

def test_function_error():
    with pytest.raises(ValueError):
        function("invalid")
```

### Running Tests
```bash
pytest                          # Run all tests
pytest tests/test_specific.py  # Run specific test file
pytest -v                       # Verbose output
pytest --cov                    # With coverage
```

## Areas for Contribution

### High Priority
- [ ] Voice input integration (Whisper)
- [ ] Better error recovery mechanisms
- [ ] Performance optimizations
- [ ] Unit and integration tests

### Medium Priority
- [ ] Browser automation plugin
- [ ] More LLM model support
- [ ] Advanced UI detection improvements
- [ ] Multi-platform testing

### Low Priority
- [ ] Documentation improvements
- [ ] Example scripts
- [ ] Video tutorials
- [ ] Community templates

## Reporting Issues

### Bug Reports
Include:
- Python version
- OS and OS version
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error logs (from `logs/screen_pilot.log`)
- Screenshots if applicable

### Feature Requests
Include:
- Clear description of desired feature
- Use cases and examples
- How it aligns with project goals
- Potential implementation approach

## Documentation

### Types of Documentation
1. **README.md**: Overview, quickstart, basic usage
2. **Code Comments**: Explain why, not what
3. **Docstrings**: Function/class documentation
4. **ARCHITECTURE.md**: System design and structure
5. **Examples/**: Practical usage examples

### Documentation Standards
```python
def analyze_screenshot(image: np.ndarray, ocr_text: str = "") -> Dict:
    """
    Analyze screenshot and extract UI information.
    
    Combines OCR results and vision analysis to understand
    the current state of the screen for action planning.
    
    Args:
        image: Screenshot as numpy array (BGR format)
        ocr_text: Pre-extracted OCR text (optional optimization)
    
    Returns:
        Dictionary containing:
        - 'app': Name of active application
        - 'elements': List of detected UI elements
        - 'state': Current application state
        - 'confidence': Confidence score of analysis
    
    Raises:
        ValueError: If image array is invalid
        ConnectionError: If API call fails
        
    Examples:
        >>> screenshot = capture_screen()
        >>> analysis = analyze_screenshot(screenshot)
        >>> print(analysis['app'])
        'Google Chrome'
    """
```

## Pull Request Process

1. **Ensure tests pass**: `pytest`
2. **Code quality checks**: `black . && flake8 . && mypy .`
3. **Update documentation** if needed
4. **Provide clear PR description** with:
   - What changes were made
   - Why these changes are needed
   - How to test the changes
   - Any breaking changes

5. **Respond to review feedback** promptly
6. **Squash commits** if requested before merge

## Community

- **Discussions**: GitHub Discussions for questions
- **Issues**: Bug reports and feature requests
- **Email**: support@screenpilot.dev
- **Twitter**: [@ScreenPilotAI](https://twitter.com/screenpilotai)

## Code of Conduct

### Our Pledge
We are committed to providing a welcoming and inclusive environment for all contributors.

### Our Standards
- Use welcoming and inclusive language
- Be respectful of differing opinions and experiences
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

### Unacceptable Behavior
- Harassment or discrimination
- Offensive comments
- Deliberate intimidation
- Other unethical conduct

### Enforcement
Violations will be addressed by project maintainers. Serious or repeated violations may result in removal from the project.

## Questions?

- Check existing issues and discussions
- Review documentation
- Search closed PRs for similar topics
- Ask in GitHub Discussions
- Email support@screenpilot.dev

## Recognition

Contributors will be:
- Added to README contributors section
- Credited in release notes
- Featured in community highlights
- Given maintainer status for sustained contributions

Thank you for contributing to Screen-Pilot! 🎉
