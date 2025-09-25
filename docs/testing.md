# Furby Therapist Testing Guide

This document covers all the ways to run tests in the Furby Therapist project, following Python testing best practices.

## Quick Start

### Recommended Methods

**Method 1: Using Make Commands (Easiest)**
```bash
# Run all tests
make test

# Run all tests with maximum verbosity
make test-verbose

# Run unit tests only (core, cli, models, features)
make test-unit

# Run integration tests only
make test-integration

# Run tests by category
make test-core              # Core library tests
make test-cli               # CLI tests
make test-models            # Model tests
make test-features          # Feature tests

# Run specific test module
make test-module MODULE=test_library

# Test basic functionality
make test-functionality

# Get help with all available commands
make help
```

**Method 2: Using unittest (Direct)**
```bash
# Run all tests
python3 -m unittest discover tests -v

# Run specific test file
python3 -m unittest tests.core.test_library -v

# Run specific test class
python3 -m unittest tests.core.test_library.TestFurbyTherapistLibrary -v

# Run specific test method
python3 -m unittest tests.core.test_library.TestFurbyTherapistLibrary.test_initialization -v
```

**Method 3: Using Test Runner Script (Advanced)**
```bash
# Run all tests
python3 tests/test_runner.py

# Run specific module
python3 tests/test_runner.py --module test_library

# Run only unit tests
python3 tests/test_runner.py --unit

# Run only integration tests
python3 tests/test_runner.py --integration
```

## Test Organization

### Test Structure
```
tests/
├── __init__.py
├── test_library.py          # Core library tests
├── test_processor.py        # Query processing tests
├── test_matcher.py          # Keyword matching tests
├── test_responses.py        # Response generation tests
├── test_models.py           # Data model tests
├── test_integration.py      # End-to-end integration tests
├── test_cycling_mode.py     # Cycling mode specific tests
├── test_bicycle_culture.py  # Bicycle culture tests
├── test_furbish_authenticity.py # Furbish language tests
├── test_greetings.py        # Greeting functionality tests
└── test_error_handling.py   # Error handling tests
```

### Test Categories

**Unit Tests**: Test individual components in isolation
- `test_library.py` - Core library functionality
- `test_processor.py` - Text processing
- `test_matcher.py` - Keyword matching
- `test_responses.py` - Response generation
- `test_models.py` - Data models

**Integration Tests**: Test component interactions
- `test_integration.py` - End-to-end workflows
- `test_cycling_mode.py` - Cycling mode integration

**Feature Tests**: Test specific features
- `test_bicycle_culture.py` - Bicycle culture features
- `test_furbish_authenticity.py` - Furbish language accuracy
- `test_greetings.py` - Greeting functionality

## Advanced Testing

### Using pytest (Alternative)

While the project uses unittest as the standard, you can also use pytest:

```bash
# Install pytest
pip install pytest pytest-cov

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=furby_therapist --cov-report=html

# Run specific test file
pytest tests/test_library.py -v

# Run tests matching a pattern
pytest tests/ -k "test_library" -v

# Run tests with specific markers (if configured)
pytest tests/ -m "unit" -v
```

### Using tox (Multi-environment Testing)

Test across multiple Python versions:

```bash
# Install tox
pip install tox

# Run tests on all configured Python versions
tox

# Run tests on specific Python version
tox -e py311

# Run with coverage
tox -e coverage

# Run linting
tox -e lint
```

### Coverage Testing

**Using coverage.py:**
```bash
# Install coverage
pip install coverage

# Run tests with coverage
coverage run -m unittest discover tests

# Generate coverage report
coverage report -m

# Generate HTML coverage report
coverage html
# Open htmlcov/index.html in browser
```

**Using pytest-cov:**
```bash
# Run with coverage
pytest tests/ --cov=furby_therapist --cov-report=term-missing

# Generate HTML report
pytest tests/ --cov=furby_therapist --cov-report=html
```

## Test Development

### Writing New Tests

**Unit Test Example:**
```python
import unittest
from furby_therapist import FurbyTherapist

class TestNewFeature(unittest.TestCase):
    def setUp(self):
        self.therapist = FurbyTherapist()
    
    def test_new_functionality(self):
        result = self.therapist.some_method()
        self.assertIsNotNone(result)
        self.assertIn("expected", result)
    
    def tearDown(self):
        self.therapist.cleanup()
```

**Integration Test Example:**
```python
import unittest
from furby_therapist.cli.main import FurbyTherapistCLI

class TestCLIIntegration(unittest.TestCase):
    def setUp(self):
        self.cli = FurbyTherapistCLI()
    
    def test_end_to_end_workflow(self):
        response = self.cli.process_single_query("test input")
        self.assertIn("Furby says:", response)
```

### Test Best Practices

1. **Use descriptive test names**
   ```python
   def test_process_query_returns_valid_response_for_sad_input(self):
   ```

2. **Follow AAA pattern** (Arrange, Act, Assert)
   ```python
   def test_example(self):
       # Arrange
       therapist = FurbyTherapist()
       
       # Act
       result = therapist.process_query("test")
       
       # Assert
       self.assertIsNotNone(result)
   ```

3. **Use setUp and tearDown for common initialization**
   ```python
   def setUp(self):
       self.therapist = FurbyTherapist()
   
   def tearDown(self):
       self.therapist.cleanup()
   ```

4. **Mock external dependencies**
   ```python
   from unittest.mock import patch, MagicMock
   
   @patch('furby_therapist.core.database.ResponseDatabase')
   def test_with_mocked_database(self, mock_db):
       mock_db.return_value.get_category.return_value = "test"
       # Test code here
   ```

## Continuous Integration

### GitHub Actions Example

Create `.github/workflows/test.yml`:
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', 3.11]
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e .[test]
    
    - name: Run tests
      run: |
        python -m unittest discover tests -v
    
    - name: Run coverage
      run: |
        pip install coverage
        coverage run -m unittest discover tests
        coverage xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
```

## Troubleshooting Tests

### Common Issues

**Import Errors:**
```bash
# Make sure you're in the project root
cd /path/to/furby-therapist

# Run tests with proper Python path
PYTHONPATH=. python3 -m unittest discover tests -v
```

**Module Not Found:**
```bash
# Install in development mode
pip install -e .

# Or use the test runner script
python3 test_runner.py
```

**Test Failures After Refactoring:**
```bash
# Update import paths in test files
# Check that mocked paths match new module structure
```

### Debug Mode

**Run single test with debugging:**
```python
import unittest
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Run specific test
if __name__ == '__main__':
    unittest.main(argv=[''], test_module='tests.test_library', exit=False, verbosity=2)
```

**Use pdb for debugging:**
```python
import pdb; pdb.set_trace()  # Add to test code
```

## Performance Testing

### Basic Performance Tests
```python
import time
import unittest
from furby_therapist import process_single_query

class TestPerformance(unittest.TestCase):
    def test_response_time(self):
        start_time = time.time()
        response = process_single_query("test query")
        end_time = time.time()
        
        # Should respond within 1 second
        self.assertLess(end_time - start_time, 1.0)
        self.assertIsNotNone(response)
```

### Memory Usage Tests
```python
import psutil
import unittest
from furby_therapist import FurbyTherapist

class TestMemoryUsage(unittest.TestCase):
    def test_memory_usage(self):
        process = psutil.Process()
        initial_memory = process.memory_info().rss
        
        therapist = FurbyTherapist()
        for i in range(100):
            therapist.process_query(f"test query {i}")
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Should not increase memory by more than 10MB
        self.assertLess(memory_increase, 10 * 1024 * 1024)
        
        therapist.cleanup()
```

## Summary

### Recommended Testing Workflow

1. **Development**: Use `make test` or `python3 -m unittest discover tests -v`
2. **Specific Testing**: Use `make test-module MODULE=test_name`
3. **CI/CD**: Use `tox` for multi-environment testing
4. **Coverage**: Use `coverage` or `pytest-cov` for coverage reports
5. **Performance**: Add performance tests for critical paths

### Quick Commands Reference

```bash
# Most common commands
make test                    # Run all tests
make test-unit              # Run unit tests only
make test-integration       # Run integration tests only
python3 test_runner.py      # Custom test runner
python3 -m unittest discover tests -v  # Standard unittest

# Coverage
coverage run -m unittest discover tests
coverage report -m

# Multi-environment
tox                         # Test all Python versions
tox -e py311               # Test specific version
```

The testing setup follows Python best practices and provides multiple ways to run tests depending on your needs and environment.