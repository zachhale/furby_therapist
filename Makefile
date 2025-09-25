# Furby Therapist Makefile
# Standard commands for development and testing

.PHONY: help test test-unit test-integration test-verbose clean install dev-install lint format

# Default target
help:
	@echo "Furby Therapist Development Commands"
	@echo "===================================="
	@echo ""
	@echo "Testing:"
	@echo "  make test              Run all tests"
	@echo "  make test-unit         Run unit tests only"
	@echo "  make test-integration  Run integration tests only"
	@echo "  make test-verbose      Run tests with verbose output"
	@echo "  make test-module MODULE=test_library  Run specific test module"
	@echo "  make test-functionality Test basic functionality"
	@echo "  make test-installation Test installation methods"
	@echo ""
	@echo "Installation:"
	@echo "  make install           Install package"
	@echo "  make dev-install       Install in development mode"
	@echo "  make install-build-tools Install build and distribution tools"
	@echo ""
	@echo "Build & Distribution:"
	@echo "  make build             Build both wheel and source distribution"
	@echo "  make build-wheel       Build wheel package only"
	@echo "  make build-sdist       Build source distribution only"
	@echo "  make check-dist        Check distribution packages"
	@echo "  make upload-test       Upload to Test PyPI"
	@echo "  make upload            Upload to PyPI"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint              Run code linting (if available)"
	@echo "  make format            Format code (if available)"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean             Clean up build artifacts"
	@echo "  make run-cli           Run CLI in interactive mode"
	@echo "  make run-cli-bikes     Run CLI in cycling mode"
	@echo "  make run-executable    Test executable script"

# Testing targets
test:
	@echo "Running all tests..."
	python3 -m unittest discover tests -v

test-unit:
	@echo "Running unit tests..."
	python3 tests/test_runner.py --unit

test-integration:
	@echo "Running integration tests..."
	python3 tests/test_runner.py --integration

test-core:
	@echo "Running core library tests..."
	python3 -m unittest discover tests/core -v

test-cli:
	@echo "Running CLI tests..."
	python3 -m unittest discover tests/cli -v

test-models:
	@echo "Running model tests..."
	python3 -m unittest discover tests/models -v

test-features:
	@echo "Running feature tests..."
	python3 -m unittest discover tests/features -v

test-verbose:
	@echo "Running tests with maximum verbosity..."
	python3 -m unittest discover tests -v -s tests -p "test_*.py"

test-module:
	@echo "Running test module: $(MODULE)"
	python3 tests/test_runner.py --module $(MODULE)

# Installation targets
install:
	pip install .

dev-install:
	pip install -e .

# Code quality targets (optional - add tools as needed)
lint:
	@echo "Linting not configured yet. Add flake8, pylint, or similar."

format:
	@echo "Formatting not configured yet. Add black, autopep8, or similar."

# Build and distribution targets
build:
	@echo "Building distribution packages..."
	@python3 -c "import build" 2>/dev/null || (echo "Build tools not installed. Run: make install-build-tools" && false)
	python3 -m build

build-wheel:
	@echo "Building wheel package..."
	@python3 -c "import build" 2>/dev/null || (echo "Build tools not installed. Run: make install-build-tools" && false)
	python3 -m build --wheel

build-sdist:
	@echo "Building source distribution..."
	@python3 -c "import build" 2>/dev/null || (echo "Build tools not installed. Run: make install-build-tools" && false)
	python3 -m build --sdist

check-dist:
	@echo "Checking distribution packages..."
	@python3 -c "import twine" 2>/dev/null || (echo "Twine not installed. Run: make install-build-tools" && false)
	@if [ ! -d "dist" ] || [ -z "$$(ls -A dist 2>/dev/null)" ]; then \
		echo "No distribution files found. Run: make build"; \
		false; \
	fi
	python3 -m twine check dist/*

upload-test:
	@echo "Uploading to Test PyPI..."
	@python3 -c "import twine" 2>/dev/null || (echo "Twine not installed. Run: make install-build-tools" && false)
	python3 -m twine upload --repository testpypi dist/*

upload:
	@echo "Uploading to PyPI..."
	@python3 -c "import twine" 2>/dev/null || (echo "Twine not installed. Run: make install-build-tools" && false)
	python3 -m twine upload dist/*

# Installation targets with build tools
install-build-tools:
	@echo "Installing build tools..."
	@echo "Note: This may require a virtual environment on some systems"
	@if python3 -c "import sys; exit(0 if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else 1)" 2>/dev/null; then \
		echo "Virtual environment detected, installing build tools..."; \
		pip install build twine setuptools wheel; \
	else \
		echo "No virtual environment detected. Trying user installation..."; \
		python3 -m pip install --user build twine setuptools wheel 2>/dev/null || \
		(echo "User installation failed. Please use a virtual environment:" && \
		 echo "  python3 -m venv venv" && \
		 echo "  source venv/bin/activate" && \
		 echo "  make install-build-tools" && \
		 false); \
	fi

# Utility targets
clean:
	@echo "Cleaning up build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

run-cli:
	@echo "Starting Furby Therapist CLI..."
	python3 -m furby_therapist

run-cli-bikes:
	@echo "Starting Furby Therapist CLI in cycling mode..."
	python3 -m furby_therapist --bikes

run-executable:
	@echo "Testing executable script..."
	./furby_therapist_cli --query "Hello from executable script!"

# Quick functionality test
test-functionality:
	@echo "Testing basic functionality..."
	python3 -c "from furby_therapist import process_single_query; print('✓ Library import works'); response = process_single_query('test'); print('✓ Basic functionality works')"

test-installation:
	@echo "Testing installation methods..."
	@echo "1. Testing module execution..."
	python3 -m furby_therapist --query "Testing module execution"
	@echo "2. Testing executable script..."
	./furby_therapist_cli --query "Testing executable script"
	@echo "3. Testing library import..."
	python3 -c "from furby_therapist import process_single_query; print('Library import successful')"