# Furby Therapist Troubleshooting Guide

This guide covers common issues and their solutions when using the Furby Therapist CLI and library.

## Common Issues

### 1. RuntimeWarning About Module Loading

**Problem**: You see this warning when running the CLI:
```
RuntimeWarning: 'furby_therapist.cli.main' found in sys.modules after import of package 'furby_therapist.cli', but prior to execution of 'furby_therapist.cli.main'; this may result in unpredictable behaviour
```

**Cause**: Running the CLI with the wrong module path causes Python to import the module twice.

**Solution**: Use the proper entry points:

✅ **Correct Methods:**
```bash
# Method 1: Installed entry point (recommended)
furby_therapist --query "hello"

# Method 2: Python module execution
python3 -m furby_therapist --query "hello"

# Method 3: Direct script execution
python3 furby_therapist/cli/main.py --query "hello"
```

❌ **Incorrect Method (causes warning):**
```bash
# DON'T DO THIS
python3 -m furby_therapist.cli.main --query "hello"
```

### 2. Import Errors

**Problem**: You get `ImportError` or `ModuleNotFoundError` when running the CLI.

**Possible Causes & Solutions:**

#### Cause A: Not in the correct directory
```bash
# Make sure you're in the project root directory
cd /path/to/furby-therapist
python3 -m furby_therapist --query "test"
```

#### Cause B: Package not installed
```bash
# Install in development mode
pip install -e .

# Or use module execution from project root
python3 -m furby_therapist --query "test"
```

#### Cause C: Python path issues
```bash
# Add current directory to Python path
PYTHONPATH=. python3 -m furby_therapist --query "test"
```

### 3. Permission Errors During Installation

**Problem**: `pip install -e .` fails with permission errors.

**Solutions:**

#### Option A: Use Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
```

#### Option B: User Installation
```bash
pip install -e . --user
```

#### Option C: System Override (Not Recommended)
```bash
pip install -e . --break-system-packages
```

### 4. CLI Command Not Found

**Problem**: `furby_therapist: command not found` after installation.

**Cause**: The installation directory is not in your PATH.

**Solutions:**

#### Check Installation Location
```bash
pip show -f furby-therapist
```

#### Add to PATH (if needed)
```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"
```

#### Use Alternative Methods
```bash
# Use module execution instead
python3 -m furby_therapist --query "hello"
```

### 5. JSON File Loading Errors

**Problem**: Errors about missing or corrupted JSON files.

**Symptoms:**
- `FileNotFoundError: responses.json`
- `JSONDecodeError: Invalid JSON`

**Solutions:**

#### Verify File Structure
```bash
# Check that data files exist
ls furby_therapist/data/
# Should show: responses.json, cycling_responses.json, etc.
```

#### Reinstall Package
```bash
pip uninstall furby-therapist
pip install -e .
```

#### Check File Permissions
```bash
# Make sure files are readable
chmod 644 furby_therapist/data/*.json
```

### 6. Memory or Performance Issues

**Problem**: CLI is slow or uses too much memory.

**Solutions:**

#### Check System Resources
```bash
# Monitor memory usage
python3 -c "
import psutil
from furby_therapist import process_single_query
print(f'Memory before: {psutil.Process().memory_info().rss / 1024 / 1024:.1f} MB')
response = process_single_query('test')
print(f'Memory after: {psutil.Process().memory_info().rss / 1024 / 1024:.1f} MB')
"
```

#### Use Stateless Mode for Better Performance
```python
from furby_therapist import FurbyTherapist

# Stateless mode uses less memory
therapist = FurbyTherapist(maintain_session=False)
```

#### Clear Conversation History
```bash
# In interactive mode, use:
clear
# or
reset
```

### 7. Cycling Mode Not Working

**Problem**: `--bikes` flag doesn't seem to change responses.

**Verification:**
```bash
# Test cycling mode
furby_therapist --bikes --query "bike maintenance"

# Should include cycling-specific responses and metaphors
```

**Troubleshooting:**
```bash
# Check if cycling responses file exists
ls furby_therapist/data/cycling_responses.json

# Test with explicit cycling keywords
furby_therapist --bikes --query "I'm stressed about my bike geometry"
```

### 8. Interactive Mode Issues

**Problem**: Interactive mode doesn't respond to commands or exits unexpectedly.

**Solutions:**

#### Check Terminal Compatibility
```bash
# Try different terminal emulators
# Some terminals handle input differently
```

#### Use Single Query Mode Instead
```bash
# If interactive mode fails, use single queries
furby_therapist --query "your message here"
```

#### Check for Signal Handling Issues
```bash
# Try graceful exit
# In interactive mode, type: quit
# Or use Ctrl+C for immediate exit
```

## Getting Help

### Debug Information
```bash
# Get version information
furby_therapist --version

# Test basic functionality
python3 -c "from furby_therapist import process_single_query; print(process_single_query('test').formatted_output)"

# Check package installation
pip show furby-therapist
```

### Verbose Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)

from furby_therapist import process_single_query
response = process_single_query("test")
```

### Report Issues
If you encounter issues not covered here:

1. **Check the documentation**: [CLI Usage Guide](cli_usage.md)
2. **Verify your setup**: Run the debug commands above
3. **Try alternative methods**: Use different CLI execution methods
4. **Check file permissions**: Ensure all files are readable
5. **Use virtual environment**: Isolate from system Python issues

## Performance Tips

### For Regular Usage
- Use the installed entry point: `furby_therapist`
- Enable cycling mode only when needed: `--bikes`
- Use single query mode for scripting: `--query "message"`

### For Development
- Use module execution: `python3 -m furby_therapist`
- Install in development mode: `pip install -e .`
- Use virtual environments to avoid conflicts

### For Integration
- Use stateless mode for better performance: `maintain_session=False`
- Implement session cleanup in long-running applications
- Consider connection pooling for high-traffic scenarios