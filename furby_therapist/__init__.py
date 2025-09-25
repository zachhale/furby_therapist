"""
Furby Therapist - A therapeutic assistant with Furby personality.

This package provides both a core library for integration into other projects
and a CLI interface for direct command-line usage.

## Core Library Usage

For external projects that want to integrate Furby therapeutic responses:

```python
from furby_therapist import FurbyTherapist, create_furby_therapist, process_single_query

# Create a stateful therapist instance
therapist = create_furby_therapist(cycling_mode=False, stateful=True)

# Process queries
response = therapist.process_query("I'm feeling sad")
print(response.formatted_output)

# Or use the convenience function for single queries
response = process_single_query("I'm anxious", cycling_mode=False)
print(response.formatted_output)
```

## CLI Usage

### Recommended Methods:

**Method 1: Installed Entry Point (Recommended)**
```bash
furby_therapist --query "I'm feeling happy"
```

**Method 2: Python Module Execution**
```bash
python3 -m furby_therapist --query "I'm feeling happy"
```

**Method 3: Direct Script Execution (Development)**
```bash
python3 furby_therapist/cli/main.py --query "I'm feeling happy"
```

### Options:
- `--bikes`: Enable cycling mode with bike-themed responses
- `--query "text"`: Single query mode (non-interactive)
- `--help`: Show help information

## Models

Common data models are available for type hints and data structures:

```python
from furby_therapist.models import FurbyResponse, QueryAnalysis, ConversationSession
```

## Documentation

- CLI Usage Guide: docs/cli_usage.md
- Library Examples: docs/library_usage_examples.md
- API Reference: docs/library_usage.md
"""

# Import core library components for external usage
from .core import (
    FurbyTherapist,
    create_furby_therapist, 
    process_single_query,
    QueryProcessor,
    KeywordMatcher,
    ResponseEngine,
    ResponseDatabase
)

# Import models for external usage
from .models import (
    QueryAnalysis,
    FurbyResponse,
    ResponseCategory,
    ConversationTurn,
    ConversationSession
)

# Package metadata
__version__ = "1.0.0"
__author__ = "Furby Therapist Team"

# Define what gets imported with "from furby_therapist import *"
__all__ = [
    # Core library classes
    'FurbyTherapist',
    'create_furby_therapist',
    'process_single_query',
    'QueryProcessor',
    'KeywordMatcher', 
    'ResponseEngine',
    'ResponseDatabase',
    
    # Data models
    'QueryAnalysis',
    'FurbyResponse',
    'ResponseCategory',
    'ConversationTurn',
    'ConversationSession',
    
    # Package info
    '__version__',
    '__author__'
]