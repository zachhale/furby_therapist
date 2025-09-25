# Furby Therapist Installation Guide

This guide covers all methods for installing and deploying the Furby Therapist CLI and library.

## Quick Installation

### For End Users (Recommended)

```bash
# Install from PyPI (when available)
pip install furby-therapist

# Or install from source
git clone <repository-url>
cd furby-therapist
pip install .
```

### For Developers

```bash
# Clone and install in development mode
git clone <repository-url>
cd furby-therapist
pip install -e .

# Or use the Makefile
make dev-install
```

## Installation Methods

### Method 1: PyPI Installation (Production)

```bash
# Install latest stable version
pip install furby-therapist

# Install specific version
pip install furby-therapist==1.0.0

# Install with development dependencies
pip install furby-therapist[dev]

# Install with test dependencies only
pip install furby-therapist[test]
```

### Method 2: Source Installation

```bash
# Download and install from source
git clone <repository-url>
cd furby-therapist

# Standard installation
pip install .

# Development installation (editable)
pip install -e .

# With optional dependencies
pip install -e .[dev]
```

### Method 3: Direct Execution (No Installation)

```bash
# Clone repository
git clone <repository-url>
cd furby-therapist

# Run directly using executable script
./furby_therapist_cli --query "Hello Furby"

# Or run as Python module
python3 -m furby_therapist --query "Hello Furby"
```

## Verification

After installation, verify everything works:

```bash
# Test CLI entry point
furby_therapist --query "Hello Furby"

# Test library import
python3 -c "from furby_therapist import process_single_query; print('Success!')"

# Run comprehensive tests
make test-installation
```

## System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, Linux
- **Memory**: 50MB RAM
- **Storage**: 10MB disk space
- **Network**: None (fully offline operation)

### Recommended Requirements
- **Python**: 3.10 or higher
- **Memory**: 100MB RAM for interactive sessions
- **Storage**: 50MB for development installation with tests

### Dependencies
- **Runtime**: None (uses only Python standard library)
- **Development**: pytest, coverage, build tools (optional)
- **Build**: setuptools, wheel, build, twine (for distribution)

## Virtual Environment Setup

### Using venv (Recommended)

```bash
# Create virtual environment
python3 -m venv furby-env

# Activate (Linux/macOS)
source furby-env/bin/activate

# Activate (Windows)
furby-env\Scripts\activate

# Install Furby Therapist
pip install furby-therapist

# Deactivate when done
deactivate
```

### Using conda

```bash
# Create conda environment
conda create -n furby-env python=3.10

# Activate environment
conda activate furby-env

# Install Furby Therapist
pip install furby-therapist

# Deactivate when done
conda deactivate
```

## Platform-Specific Instructions

### macOS

```bash
# Install using Homebrew Python (recommended)
brew install python3
pip3 install furby-therapist

# Or using system Python
python3 -m pip install --user furby-therapist
```

### Linux (Ubuntu/Debian)

```bash
# Install Python 3 and pip
sudo apt update
sudo apt install python3 python3-pip

# Install Furby Therapist
pip3 install furby-therapist

# Add to PATH if needed
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Windows

```bash
# Using Python from python.org
python -m pip install furby-therapist

# Using Windows Store Python
python3 -m pip install furby-therapist

# Add to PATH if needed (usually automatic)
```

## Development Installation

### Full Development Setup

```bash
# Clone repository
git clone <repository-url>
cd furby-therapist

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or: venv\Scripts\activate  # Windows

# Install in development mode with all dependencies
pip install -e .[dev]

# Install build tools
make install-build-tools

# Run tests to verify setup
make test
```

### Development Workflow

```bash
# Make changes to code
# ...

# Run tests
make test

# Test functionality
make test-functionality

# Test installation methods
make test-installation

# Build distribution
make build

# Check distribution
make check-dist
```

## Troubleshooting Installation

### Common Issues

#### Permission Errors
```bash
# Use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install furby-therapist

# Or install for current user only
pip install --user furby-therapist
```

#### Python Version Issues
```bash
# Check Python version
python3 --version

# Must be 3.8 or higher
# Upgrade Python if needed
```

#### Import Errors
```bash
# Verify installation
pip list | grep furby

# Reinstall if needed
pip uninstall furby-therapist
pip install furby-therapist

# Check Python path
python3 -c "import sys; print(sys.path)"
```

#### Command Not Found
```bash
# Check if entry point is installed
pip show furby-therapist

# Add to PATH if needed (Linux/macOS)
export PATH="$HOME/.local/bin:$PATH"

# Or use module execution
python3 -m furby_therapist
```

### Getting Help

If you encounter issues:

1. **Check the troubleshooting guide**: `docs/troubleshooting.md`
2. **Run diagnostic tests**: `make test-installation`
3. **Check system requirements**: Ensure Python 3.8+
4. **Try virtual environment**: Isolate from system packages
5. **Use alternative methods**: Try different installation methods

## Uninstallation

### Remove Package
```bash
# Uninstall package
pip uninstall furby-therapist

# Remove virtual environment (if used)
rm -rf furby-env

# Remove cloned repository (if applicable)
rm -rf furby-therapist
```

### Clean System
```bash
# Remove Python cache files
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Remove build artifacts
rm -rf build/ dist/ *.egg-info/
```

## Distribution and Deployment

### For Package Maintainers

#### Building Distributions
```bash
# Install build tools
make install-build-tools

# Clean previous builds
make clean

# Build distributions
make build

# Check distributions
make check-dist
```

#### Publishing to PyPI
```bash
# Test on Test PyPI first
make upload-test

# Verify test installation
pip install -i https://test.pypi.org/simple/ furby-therapist

# Upload to production PyPI
make upload
```

#### Release Checklist
- [ ] Update version in `furby_therapist/__init__.py`
- [ ] Update version in `pyproject.toml` and `setup.py`
- [ ] Run full test suite: `make test`
- [ ] Test installation methods: `make test-installation`
- [ ] Build distributions: `make build`
- [ ] Check distributions: `make check-dist`
- [ ] Test upload to Test PyPI: `make upload-test`
- [ ] Upload to production PyPI: `make upload`
- [ ] Create GitHub release with changelog
- [ ] Update documentation

## Next Steps

After installation:

1. **Read the CLI usage guide**: `docs/cli_usage.md`
2. **Try the library examples**: `docs/library_usage_examples.md`
3. **Run some tests**: `make test-functionality`
4. **Start chatting**: `furby_therapist`

Enjoy your whimsical therapeutic conversations with Furby!