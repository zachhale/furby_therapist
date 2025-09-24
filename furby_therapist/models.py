"""
Data models for the Furby Therapist CLI system.
"""

from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class QueryAnalysis:
    """Result of analyzing a user query."""
    original_text: str
    normalized_text: str
    keywords: List[str]
    detected_emotion: str
    confidence: float
    category: str


@dataclass
class ResponseCategory:
    """A category of therapeutic responses with associated metadata."""
    name: str
    keywords: List[str]
    responses: List[str]
    furby_sounds: List[str]
    furbish_phrases: List[Tuple[str, str]]  # (furbish, translation)
    weight: float


@dataclass
class FurbyResponse:
    """A complete Furby-style therapeutic response."""
    base_message: str
    furby_sounds: List[str]
    furbish_phrase: Optional[Tuple[str, str]]
    formatted_output: str
    clean_version: Optional[str] = None  # Clean version without Furbish for repeats