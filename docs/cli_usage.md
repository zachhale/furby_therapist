# Furby Therapist CLI Usage Guide

This document covers all the ways to run the Furby Therapist CLI and explains the proper usage methods.

## Installation Methods

### Option 1: Install from Source (Recommended for Development)
```bash
# Clone the repository
git clone <repository-url>
cd furby-therapist

# Install in development mode
pip install -e .
```

### Option 2: Install from PyPI (When Available)
```bash
pip install furby-therapist
```

## CLI Usage Methods

### Method 1: Installed Entry Point (Recommended)
After installing the package, use the `furby_therapist` command:

```bash
# Interactive mode
furby_therapist

# Single query mode
furby_therapist --query "I'm feeling sad"

# Cycling mode
furby_therapist --bikes

# Cycling mode with single query
furby_therapist --bikes --query "I'm stressed about performance"

# Help
furby_therapist --help
```

### Method 2: Python Module Execution
Run the package as a Python module:

```bash
# Interactive mode
python3 -m furby_therapist

# Single query mode
python3 -m furby_therapist --query "I'm feeling anxious"

# Cycling mode
python3 -m furby_therapist --bikes

# Help
python3 -m furby_therapist --help
```

### Method 3: Direct Script Execution (Development)
For development or when you haven't installed the package:

```bash
# Interactive mode
python3 furby_therapist/cli/main.py

# Single query mode
python3 furby_therapist/cli/main.py --query "Hello Furby"

# Cycling mode
python3 furby_therapist/cli/main.py --bikes

# Help
python3 furby_therapist/cli/main.py --help
```

## Command Line Options

### Basic Options
- `--query`, `-q`: Process a single query and exit (non-interactive mode)
- `--bikes`: Enable cycling mode with bike-themed therapeutic responses
- `--version`: Show version information
- `--help`, `-h`: Show help message

### Examples

#### Standard Therapeutic Mode
```bash
# Interactive conversation
furby_therapist

# Single therapeutic response
furby_therapist --query "I'm feeling overwhelmed at work"
```

#### Cycling Mode
```bash
# Interactive cycling-themed therapy
furby_therapist --bikes

# Single cycling-themed response
furby_therapist --bikes --query "I'm nervous about my first century ride"
```

## Interactive Mode Commands

When running in interactive mode, you can use these special commands:

- `help` or `?`: Show help menu
- `repeat`: Ask Furby to repeat the last response more clearly
- `clear` or `reset`: Start a fresh conversation
- `quit`, `exit`, `bye`, `goodbye`: End the session

## Troubleshooting

### RuntimeWarning About Module Loading
If you see a warning like:
```
RuntimeWarning: 'furby_therapist.cli.main' found in sys.modules...
```

**Solution**: Use the proper entry points listed above. Avoid running:
```bash
# DON'T DO THIS - causes warnings
python3 -m furby_therapist.cli.main
```

**Instead use**:
```bash
# DO THIS - no warnings
python3 -m furby_therapist
# OR
furby_therapist
```

### Import Errors
If you get import errors when running directly:

1. **Make sure you're in the project root directory**
2. **Use the module execution method**: `python3 -m furby_therapist`
3. **Or install the package**: `pip install -e .`

### Permission Issues on macOS/Linux
If you get permission errors when installing:

```bash
# Use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install -e .

# Or install for current user only
pip install -e . --user
```

## Development Usage

### Running Tests
```bash
# Run all tests
python3 -m unittest discover tests

# Run specific test file
python3 -m unittest tests.test_library

# Run with verbose output
python3 -m unittest discover tests -v
```

### Library Development
```bash
# Test library imports
python3 -c "from furby_therapist import FurbyTherapist; print('Success')"

# Test CLI imports
python3 -c "from furby_therapist.cli.main import main; print('Success')"
```

## Integration with Other Tools

### Shell Aliases
Add to your `.bashrc` or `.zshrc`:
```bash
alias furby="furby_therapist"
alias furby-bikes="furby_therapist --bikes"
```

### Scripting
```bash
#!/bin/bash
# Get a quick therapeutic response
response=$(furby_therapist --query "$1")
echo "$response"
```

### IDE Integration
Most IDEs can run the CLI directly:
- **VS Code**: Use integrated terminal with any of the methods above
- **PyCharm**: Configure run configuration with `furby_therapist` as the script
- **Vim/Neovim**: Use `:!furby_therapist --query "your message"`

## Performance Notes

- **Startup Time**: ~0.5-1 second for single queries
- **Memory Usage**: ~10-20MB for typical sessions
- **Offline Operation**: No network connectivity required
- **Session Memory**: Conversation history maintained in interactive mode

## Best Practices

1. **Use the installed entry point** (`furby_therapist`) for regular usage
2. **Use module execution** (`python3 -m furby_therapist`) for development
3. **Enable cycling mode** (`--bikes`) if you're a cycling enthusiast
4. **Use single query mode** (`--query`) for scripting and automation
5. **Clear conversation history** (`clear` command) for fresh starts in interactive mode