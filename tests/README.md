# Furby Therapist Test Suite

This directory contains a comprehensive test suite for the Furby Therapist project, covering unit tests, integration tests, performance tests, and manual test scenarios.

## Test Structure

```
tests/
├── cli/                    # CLI-specific tests
├── core/                   # Core library component tests
├── features/               # Feature-specific tests
├── integration/            # Integration and end-to-end tests
├── manual/                 # Manual test scenarios
├── models/                 # Data model tests
├── performance/            # Performance and stress tests
└── test_runner.py         # Test runner script
```

## Test Categories

### Unit Tests (`tests/core/`, `tests/cli/`, `tests/models/`, `tests/features/`)

**Purpose**: Test individual components in isolation

**Coverage**:
- `test_processor.py`: Query processing, text normalization, emotion detection
- `test_matcher.py`: Keyword matching, category selection, confidence scoring
- `test_responses.py`: Response generation, Furby personality, caching
- `test_library.py`: Library interface, convenience functions, session management
- `test_database.py`: Response database loading, category management
- `test_main.py`: CLI functionality, argument parsing
- `test_models.py`: Data model validation
- `test_bicycle_culture.py`: Cycling keyword handling
- `test_furbish_authenticity.py`: Furbish phrase validation
- `test_greetings.py`: Morning/night greeting functionality

**Run with**: `python3 tests/test_runner.py --unit`

### Integration Tests (`tests/integration/`)

**Purpose**: Test component interactions and complete workflows

**Coverage**:
- `test_integration.py`: Core pipeline integration, component data flow
- `test_error_handling.py`: Comprehensive error handling across all components
- `test_therapeutic_quality.py`: Therapeutic appropriateness and Furby authenticity validation
- `test_end_to_end.py`: Library interface workflows and CLI entry point testing

**Run with**: `python3 tests/test_runner.py --integration`

### Performance Tests (`tests/performance/`)

**Purpose**: Test system performance, response times, and resource usage

**Coverage**:
- Response time benchmarks
- Memory usage stability
- Concurrent instance handling
- Large input processing
- Stress testing with rapid queries
- Session longevity testing

**Run with**: `python3 tests/test_runner.py --performance`

### Manual Tests (`tests/manual/`)

**Purpose**: Human evaluation of therapeutic quality and Furby authenticity

**Coverage**:
- Emotional sensitivity scenarios
- Boundary appropriateness
- Furby personality authenticity
- Cultural sensitivity
- Cycling mode appropriateness
- Repeat functionality quality

**Run with**: `python3 tests/test_runner.py --manual`

## Running Tests

### All Tests
```bash
python3 tests/test_runner.py
# or
python3 -m unittest discover tests
```

### Specific Test Categories
```bash
# Unit tests only
python3 tests/test_runner.py --unit

# Integration tests only
python3 tests/test_runner.py --integration

# Performance tests only
python3 tests/test_runner.py --performance

# Manual test scenarios
python3 tests/test_runner.py --manual
```

### Specific Test Module
```bash
# Run specific test file
python3 tests/test_runner.py --module test_library

# Run with unittest directly
python3 -m unittest tests.core.test_library
```

### Using Make (if available)
```bash
# Run all tests
make test

# Run specific test categories
make test-unit
make test-integration
make test-performance
```

## Test Requirements

### Prerequisites
- Python 3.7+
- All project dependencies installed
- `responses.json` file present (for integration tests)

### Optional Dependencies
- `psutil` for memory monitoring tests
- `unittest.mock` (included in Python 3.3+)

## Test Coverage Areas

### Core Functionality
- [x] Query processing and text normalization
- [x] Keyword matching and categorization
- [x] Response generation and formatting
- [x] Furby personality elements
- [x] Furbish phrase authenticity
- [x] Error handling and recovery
- [x] Caching and repeat functionality

### CLI Interface
- [x] Argument parsing
- [x] Interactive mode
- [x] Single query mode
- [x] Cycling mode toggle
- [x] Output formatting
- [x] Signal handling

### Library Interface
- [x] Stateful and stateless modes
- [x] Session management
- [x] Conversation history
- [x] Convenience functions
- [x] Error handling
- [x] Resource cleanup

### Therapeutic Quality
- [x] Emotional support appropriateness
- [x] Validation and empathy
- [x] Boundary maintenance
- [x] Crisis situation handling
- [x] Cultural sensitivity
- [x] Encouragement and hope

### Furby Authenticity
- [x] Personality elements
- [x] Sound effects authenticity
- [x] Furbish phrase validation
- [x] Whimsical but appropriate tone
- [x] Therapeutic balance

### Performance
- [x] Response time benchmarks
- [x] Memory usage monitoring
- [x] Concurrent usage
- [x] Large input handling
- [x] Stress testing
- [x] Session longevity

## Test Data

### Mock Data
Tests use temporary files and mock objects to avoid dependencies on external files.

### Real Data Integration
Some integration tests can use actual `responses.json` files when available, but gracefully skip when missing.

### Edge Cases
Comprehensive edge case testing including:
- Empty inputs
- Invalid data types
- Malformed JSON
- Large inputs
- Special characters
- Unicode content

## Manual Test Evaluation

The manual tests generate scenarios that require human evaluation for:

1. **Therapeutic Appropriateness**: Are responses supportive without being dismissive?
2. **Emotional Sensitivity**: Do responses validate feelings appropriately?
3. **Boundary Maintenance**: Are professional boundaries maintained?
4. **Furby Authenticity**: Does the personality feel genuinely Furby-like?
5. **Cultural Sensitivity**: Are responses inclusive and respectful?

### Manual Test Process
1. Run manual tests: `python3 tests/test_runner.py --manual`
2. Review printed scenarios and responses
3. Evaluate each response against the criteria
4. Document any issues or improvements needed

## Continuous Integration

### Test Automation
- All unit and integration tests should pass in CI
- Performance tests can be run periodically
- Manual tests require human review

### Coverage Goals
- Unit test coverage: >90%
- Integration test coverage: >80%
- Critical path coverage: 100%

## Contributing Tests

### Adding New Tests
1. Choose appropriate test category (unit/integration/performance/manual)
2. Follow existing naming conventions (`test_*.py`)
3. Include docstrings explaining test purpose
4. Use appropriate assertions and error messages
5. Clean up resources in tearDown methods

### Test Guidelines
- Tests should be independent and repeatable
- Use descriptive test names and subTest contexts
- Mock external dependencies appropriately
- Test both success and failure scenarios
- Include edge cases and boundary conditions

### Performance Test Guidelines
- Set reasonable time limits based on expected usage
- Test with realistic data sizes
- Monitor resource usage trends
- Include stress testing scenarios

### Manual Test Guidelines
- Provide clear evaluation criteria
- Include diverse scenarios
- Format output for easy human review
- Document expected outcomes