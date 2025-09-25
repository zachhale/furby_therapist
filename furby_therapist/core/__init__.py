"""
Furby Therapist Core Library - Core functionality for generating Furby-style therapeutic responses.

This module provides the core library functionality that can be imported and used
by external projects, separate from CLI-specific code.
"""

from .library import FurbyTherapist, create_furby_therapist, process_single_query
from .processor import QueryProcessor
from .matcher import KeywordMatcher
from .responses import ResponseEngine
from .database import ResponseDatabase

__all__ = [
    'FurbyTherapist',
    'create_furby_therapist', 
    'process_single_query',
    'QueryProcessor',
    'KeywordMatcher',
    'ResponseEngine',
    'ResponseDatabase'
]