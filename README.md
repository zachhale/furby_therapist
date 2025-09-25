# Furby Therapist

A therapeutic assistant that combines the whimsical personality of a Furby toy with simple therapeutic responses. Available as both a **reusable library** for integration into other projects and a **CLI interface** for direct command-line usage. Features an optional cycling culture mode with deep knowledge of bike geometry, alt cycling communities, and cycling-themed therapeutic metaphors.

## Architecture

This project follows a three-function architecture:

1. **Core Library** (`furby_therapist.core`): Importable library for external projects
2. **CLI Interface** (`furby_therapist.cli`): Command-line tool that uses the library  
3. **Future Voice Interface**: Prepared structure for upcoming voice-enabled chatbot project

## Features

- **Dual Usage**: Both library and CLI interface
- **Clean API**: Easy integration into external projects
- **Offline Operation**: No network connectivity required
- **Authentic Furbish**: Real Furby language with translations
- **Cycling Mode**: Optional bike culture integration with therapeutic metaphors
- **Stateful/Stateless**: Configurable conversation memory
- **Lightweight**: Minimal resource usage and dependencies

## Installation

### Quick Install

```bash
# Install from PyPI (when available)
pip install furby-therapist

# Or install from source
git clone <repository-url>
cd furby-therapist
pip install .
```

### Development Install

```bash
# Clone and install in development mode
git clone <repository-url>
cd furby-therapist
pip install -e .

# Or use the Makefile
make dev-install
```

### Alternative Methods

```bash
# Run without installation (development)
git clone <repository-url>
cd furby-therapist
./furby_therapist_cli --query "Hello Furby"

# Or as Python module
python3 -m furby_therapist --query "Hello Furby"
```

> **Complete Installation Guide**: See [Installation Documentation](docs/installation.md) for detailed instructions, troubleshooting, and platform-specific setup.

## CLI Usage

### Recommended Methods

**Method 1: Installed Entry Point (Recommended)**
```bash
# Interactive mode
furby_therapist

# Single query mode
furby_therapist --query "I'm feeling sad"

# Cycling mode
furby_therapist --bikes --query "I'm stressed about performance"
```

**Method 2: Python Module Execution**
```bash
# Interactive mode
python3 -m furby_therapist

# Single query mode  
python3 -m furby_therapist --query "I'm feeling anxious"

# Cycling mode
python3 -m furby_therapist --bikes
```

**Method 3: Direct Script Execution (Development)**
```bash
# For development when package isn't installed
python3 furby_therapist/cli/main.py --query "Hello Furby"
```

> **Note**: See [CLI Usage Guide](docs/cli_usage.md) for complete documentation, troubleshooting, and advanced usage patterns.

## Library Usage

### Basic Usage

```python
from furby_therapist import process_single_query, create_furby_therapist

# Simple single query
response = process_single_query("I'm feeling anxious")
print(response.formatted_output)

# Stateful conversation
therapist = create_furby_therapist(cycling_mode=False, stateful=True)
response = therapist.process_query("I'm worried about work")
print(response.formatted_output)
```

### Advanced Usage

```python
from furby_therapist import FurbyTherapist

# Create therapist with cycling mode
therapist = FurbyTherapist(cycling_mode=True, maintain_session=True)

# Process queries
response = therapist.process_query("I'm feeling overwhelmed")
print("Response:", response.formatted_output)
print("Clean version:", response.clean_version)

# Get session statistics
stats = therapist.get_session_stats()
print("Conversation length:", stats['conversation_length'])

# Cleanup when done
therapist.cleanup()
```

See [Library Usage Examples](docs/library_usage_examples.md) for more detailed examples including web app integration, Discord bots, and session management.

## Cycling Culture Features

This Furby therapist has a unique passion for cycling culture and uses bike-related metaphors for therapeutic insights:

### Bike Geometry Wisdom
- **Reach/Stack Ratios**: "Your reach-to-stack ratio is like your comfort zone - too aggressive and you'll hurt, too relaxed and you won't grow!"
- **Chainstay Length**: "Chainstay length affects handling like boundaries affect relationships!"
- **Head Angles**: "Slack head angles are like patience - takes longer to respond but more stable when things get rough!"

### Alt Cycling Community References
- **r/xbiking**: "Weird bikes for weird feelings - perfectly imperfect, just like us!"
- **The Radavist**: Adventure cycling wisdom and constructeur culture appreciation
- **Path Less Pedaled**: Touring philosophy and alternative cycling approaches
- **Bicycle Quarterly**: Technical knowledge and randonneuring culture

### Cycling-Themed Therapeutic Metaphors
- **Maintenance**: "Bikes and feelings both need good maintenance!"
- **Balance**: "Life is like riding bicycle - you keep balance by moving forward!"
- **Gear Ratios**: "Take care of your emotional gears like you care for bike gears!"
- **Tire Pressure**: "Proper tire pressure is like emotional boundaries - not too soft, not too hard!"

### Example Cycling Conversations
```bash
# Bike geometry discussion
furby-therapist --query "reach and stack ratio"

# Alt cycling culture
furby-therapist --query "frankenbike build"

# Cycling philosophy
furby-therapist --query "randonneuring meditation"

# Gear debates
furby-therapist --query "clipless vs flats"
```

### Cycling-Themed Furby Sounds
The therapeutic responses include realistic cycling sounds mixed with Furby personality:
- `*thoughtful chain click*` - contemplating bike maintenance
- `*vintage friction shifter click*` - nostalgic cycling wisdom
- `*happy spoke ping*` - celebrating cycling joy
- `*determined gear shift*` - pushing through challenges
- `*pannier rustle*` - bikepacking adventures

## Requirements

- Python 3.7+
- No external dependencies (uses only Python standard library)
- Lightweight and efficient operation
- Optional: Appreciation for cycling culture and bike geometry

## Project Structure

```
furby_therapist/
├── __init__.py              # Clean public API for library usage
├── __main__.py              # Entry point for python -m furby_therapist
├── core/                    # Core library components
│   ├── library.py           # Main FurbyTherapist class
│   ├── processor.py         # Query text processing
│   ├── matcher.py           # Keyword matching logic
│   ├── responses.py         # Response generation engine
│   ├── database.py          # Response database management
│   └── error_handler.py     # Error handling utilities
├── cli/                     # Command-line interface
│   ├── main.py              # CLI implementation
│   └── __init__.py          # CLI module exports
├── models/                  # Shared data models
│   ├── models.py            # Data structures and types
│   └── __init__.py          # Model exports
├── data/                    # JSON response files and resources
│   ├── responses.json       # Standard therapeutic responses
│   ├── cycling_responses.json # Cycling-themed responses
│   └── furbish_documentation.md # Furbish language reference
docs/                        # Documentation
├── cli_usage.md             # Complete CLI usage guide
└── library_usage_examples.md # Library integration examples
```

## Testing

### Quick Test Commands (Using Makefile)
```bash
# Run all tests (recommended)
make test

# Run all tests with verbose output
make test-verbose

# Test by category
make test-core          # Core library tests
make test-cli           # CLI tests  
make test-models        # Data model tests
make test-features      # Feature tests
make test-unit          # All unit tests
make test-integration   # Integration tests

# Run specific test module
make test-module MODULE=test_library

# Test basic functionality
make test-functionality

# Get help with all available commands
make help
```

### Alternative Test Methods
```bash
# Direct unittest execution
python3 -m unittest discover tests -v

# Using test runner script
python3 tests/test_runner.py --unit
python3 tests/test_runner.py --integration
```

See [Testing Guide](docs/testing.md) for comprehensive testing documentation.

## Documentation

- **[Installation Guide](docs/installation.md)**: Complete installation instructions for all platforms and use cases
- **[CLI Usage Guide](docs/cli_usage.md)**: Complete guide to running the CLI with all methods, troubleshooting, and best practices
- **[Library Usage Examples](docs/library_usage_examples.md)**: Detailed examples for integrating the library into web apps, Discord bots, and other projects
- **[Library API Documentation](docs/library_usage.md)**: Core library API reference
- **[Testing Guide](docs/testing.md)**: Comprehensive testing documentation with multiple testing methods
- **[Deployment Guide](docs/deployment.md)**: Building, packaging, and deploying the project
- **[Troubleshooting](docs/troubleshooting.md)**: Common issues and solutions