# Python Command Standards

## Python Executable
Always use `python3` instead of `python` when running Python commands or scripts in this project.

## Testing Framework
Use `unittest` instead of `pytest` for running tests in this project.

Examples:
- Use `python3 main.py` instead of `python main.py`
- Use `python3 -m unittest` instead of `python3 -m pytest`
- Use `python3 -m unittest discover` for test discovery
- Use `python3 -m pip install` instead of `python -m pip install`

This ensures compatibility and uses the correct Python version and testing framework across different environments.