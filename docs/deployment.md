# Furby Therapist Deployment Guide

This guide covers building, packaging, and deploying the Furby Therapist CLI and library.

## Quick Deployment

### Using the Deployment Script (Recommended)

```bash
# Build package
python3 scripts/deploy.py

# Build and test installation
python3 scripts/deploy.py --test
```

### Using Makefile

```bash
# Install build tools (may require virtual environment)
make install-build-tools

# Build package
make build

# Check package
make check-dist
```

## Deployment Methods

### Method 1: Automated Deployment Script

The deployment script handles everything automatically:

```bash
# Basic deployment
python3 scripts/deploy.py

# With installation testing
python3 scripts/deploy.py --test
```

**What it does:**
- Checks Python version compatibility
- Installs build tools if needed
- Cleans previous build artifacts
- Builds wheel and source distributions
- Validates package integrity
- Optionally tests installation

### Method 2: Manual Deployment

#### Step 1: Install Build Tools

```bash
# In a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install build twine setuptools wheel

# Or system-wide (if allowed)
pip install build twine setuptools wheel
```

#### Step 2: Clean and Build

```bash
# Clean previous builds
make clean

# Build distributions
python3 -m build

# Or build specific types
python3 -m build --wheel    # Wheel only
python3 -m build --sdist    # Source distribution only
```

#### Step 3: Validate Package

```bash
# Check package integrity
python3 -m twine check dist/*

# List built files
ls -la dist/
```

### Method 3: Using Makefile Commands

```bash
# Complete build process
make clean
make build
make check-dist

# Individual steps
make build-wheel     # Build wheel only
make build-sdist     # Build source distribution only
```

## Package Structure

After building, you'll have these files in `dist/`:

```
dist/
├── furby_therapist-1.0.0-py3-none-any.whl    # Wheel distribution
└── furby_therapist-1.0.0.tar.gz              # Source distribution
```

### Wheel Distribution (.whl)
- **Purpose**: Fast installation for end users
- **Contains**: Compiled Python code and data files
- **Usage**: `pip install furby_therapist-1.0.0-py3-none-any.whl`

### Source Distribution (.tar.gz)
- **Purpose**: Installation from source, development
- **Contains**: Source code, setup files, documentation
- **Usage**: `pip install furby_therapist-1.0.0.tar.gz`

## Testing Installation

### Local Testing

```bash
# Test wheel installation
pip install dist/furby_therapist-1.0.0-py3-none-any.whl

# Test CLI
furby_therapist --query "Installation test"

# Test library
python3 -c "from furby_therapist import process_single_query; print('Success')"

# Uninstall
pip uninstall furby-therapist
```

### Virtual Environment Testing

```bash
# Create test environment
python3 -m venv test-env
source test-env/bin/activate

# Install and test
pip install dist/furby_therapist-1.0.0-py3-none-any.whl
furby_therapist --query "Test message"

# Cleanup
deactivate
rm -rf test-env
```

## Publishing to PyPI

### Prerequisites

1. **PyPI Account**: Register at https://pypi.org
2. **API Token**: Generate at https://pypi.org/manage/account/token/
3. **Twine Configuration**: Store credentials securely

### Test PyPI (Recommended First)

```bash
# Upload to Test PyPI
python3 -m twine upload --repository testpypi dist/*

# Test installation from Test PyPI
pip install -i https://test.pypi.org/simple/ furby-therapist

# Verify it works
furby_therapist --query "Test PyPI installation"
```

### Production PyPI

```bash
# Upload to production PyPI
python3 -m twine upload dist/*

# Test installation
pip install furby-therapist

# Verify
furby_therapist --version
```

### Using Makefile

```bash
# Upload to Test PyPI
make upload-test

# Upload to production PyPI
make upload
```

## Release Process

### Pre-Release Checklist

- [ ] **Update version** in `furby_therapist/__init__.py`
- [ ] **Update version** in `pyproject.toml` and `setup.py`
- [ ] **Run full test suite**: `make test`
- [ ] **Test all installation methods**: `make test-installation`
- [ ] **Update documentation** if needed
- [ ] **Create changelog entry**

### Release Steps

1. **Prepare Release**
   ```bash
   # Update version numbers
   # Update documentation
   # Commit changes
   git add .
   git commit -m "Prepare release v1.0.0"
   git tag v1.0.0
   ```

2. **Build and Test**
   ```bash
   # Clean and build
   python3 scripts/deploy.py --test
   
   # Or manually
   make clean
   make build
   make check-dist
   ```

3. **Test Release**
   ```bash
   # Upload to Test PyPI
   make upload-test
   
   # Test installation
   pip install -i https://test.pypi.org/simple/ furby-therapist
   furby_therapist --query "Release test"
   ```

4. **Production Release**
   ```bash
   # Upload to PyPI
   make upload
   
   # Push to repository
   git push origin main
   git push origin v1.0.0
   ```

5. **Post-Release**
   ```bash
   # Test public installation
   pip install furby-therapist
   
   # Create GitHub release
   # Update documentation
   # Announce release
   ```

## Troubleshooting Deployment

### Build Issues

#### Missing Build Tools
```bash
# Error: ModuleNotFoundError: No module named 'build'
# Solution: Install build tools
python3 -m venv venv
source venv/bin/activate
pip install build twine setuptools wheel
```

#### Permission Errors
```bash
# Error: externally-managed-environment
# Solution: Use virtual environment
python3 -m venv venv
source venv/bin/activate
# Then retry build commands
```

#### Package Data Missing
```bash
# Error: FileNotFoundError for JSON files
# Solution: Check MANIFEST.in and package_data in setup.py
# Ensure data files are properly included
```

### Upload Issues

#### Authentication Errors
```bash
# Error: 403 Forbidden
# Solution: Check API token and credentials
python3 -m twine upload --repository testpypi dist/* --verbose
```

#### Version Conflicts
```bash
# Error: File already exists
# Solution: Update version number or use --skip-existing
python3 -m twine upload --skip-existing dist/*
```

### Installation Issues

#### Import Errors After Installation
```bash
# Error: ModuleNotFoundError after pip install
# Solution: Check package structure and __init__.py
# Verify entry points in setup.py
```

#### Command Not Found
```bash
# Error: furby_therapist: command not found
# Solution: Check entry points and PATH
pip show furby-therapist
echo $PATH
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Build and Deploy

on:
  push:
    tags:
      - 'v*'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    
    - name: Build package
      run: python -m build
    
    - name: Check package
      run: twine check dist/*
    
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

## Best Practices

### Version Management
- Use semantic versioning (MAJOR.MINOR.PATCH)
- Update version in all relevant files consistently
- Tag releases in version control

### Testing
- Always test on Test PyPI first
- Test installation in clean environments
- Verify all entry points work correctly

### Documentation
- Keep installation instructions up to date
- Document breaking changes in releases
- Provide migration guides for major versions

### Security
- Use API tokens instead of passwords
- Store credentials securely
- Regularly rotate API tokens

## Automation

### Automated Deployment Script

The `scripts/deploy.py` script automates the entire process:

```bash
# Full automated deployment
python3 scripts/deploy.py --test

# What it does:
# 1. Checks Python version
# 2. Installs build tools
# 3. Cleans build artifacts
# 4. Builds distributions
# 5. Validates packages
# 6. Tests installation (with --test flag)
```

### Makefile Integration

Use Makefile targets for common tasks:

```bash
make clean          # Clean build artifacts
make build          # Build distributions
make check-dist     # Validate packages
make upload-test    # Upload to Test PyPI
make upload         # Upload to PyPI
```

This deployment guide ensures reliable, repeatable package builds and distributions for the Furby Therapist project.