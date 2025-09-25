"""
Furby Therapist CLI - Command-line interface for the Furby Therapist.

This module provides the CLI-specific functionality for interacting with
the Furby Therapist through the command line.
"""

from .main import FurbyTherapistCLI, create_argument_parser, main

__all__ = [
    'FurbyTherapistCLI',
    'create_argument_parser',
    'main'
]