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
	@echo ""
	@echo "Installation:"
	@echo "  make install           Install package"
	@echo "  make dev-install       Install in development mode"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint              Run code linting (if available)"
	@echo "  make format            Format code (if available)"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean             Clean up build artifacts"
	@echo "  make run-cli           Run CLI in interactive mode"
	@echo "  make run-cli-bikes     Run CLI in cycling mode"

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

# Quick functionality test
test-functionality:
	@echo "Testing basic functionality..."
	python3 -c "from furby_therapist import process_single_query; print('✓ Library import works'); response = process_single_query('test'); print('✓ Basic functionality works')"