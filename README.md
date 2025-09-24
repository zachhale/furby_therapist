# Furby Therapist CLI

A therapeutic assistant that combines the whimsical personality of a Furby toy with simple therapeutic responses. Designed to run efficiently on Raspberry Pi Zero 2 W hardware.

## Features

- Offline therapeutic responses in Furby-style language
- Interactive CLI interface with continuous conversation mode
- Authentic Furbish phrases with English translations
- Lightweight design optimized for Raspberry Pi Zero 2 W
- Simple keyword-based response matching

## Installation

```bash
pip install -e .
```

## Usage

### Interactive Mode (default)
```bash
furby-therapist
```

### Single Query Mode
```bash
furby-therapist --query "how are you feeling?"
```

## Requirements

- Python 3.7+
- No external dependencies (uses only Python standard library)
- Optimized for Raspberry Pi Zero 2 W (ARM processor, <50MB RAM)

## Project Structure

```
furby_therapist/
├── __init__.py          # Package initialization
├── models.py            # Data models and structures
├── cli.py              # Command-line interface
├── processor.py        # Query text processing
├── matcher.py          # Keyword matching logic
├── responses.py        # Response generation engine
└── database.py         # Response database
```