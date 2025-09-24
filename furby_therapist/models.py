"""
Data models for the Furby Therapist CLI system.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from datetime import datetime


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


@dataclass
class ConversationTurn:
    """A single turn in the conversation (user input + Furby response)."""
    timestamp: datetime
    user_input: str
    user_emotion: str
    furby_response: str
    response_category: str


@dataclass
class ConversationSession:
    """Manages conversation history and context for a session."""
    session_start: datetime = field(default_factory=datetime.now)
    turns: List[ConversationTurn] = field(default_factory=list)
    dominant_emotions: List[str] = field(default_factory=list)
    
    def add_turn(self, user_input: str, user_emotion: str, furby_response: str, response_category: str):
        """Add a new conversation turn to the session."""
        turn = ConversationTurn(
            timestamp=datetime.now(),
            user_input=user_input,
            user_emotion=user_emotion,
            furby_response=furby_response,
            response_category=response_category
        )
        self.turns.append(turn)
        
        # Track dominant emotions (keep last 5 for context)
        if user_emotion != "neutral":
            self.dominant_emotions.append(user_emotion)
            if len(self.dominant_emotions) > 5:
                self.dominant_emotions.pop(0)
    
    def get_recent_emotions(self, count: int = 3) -> List[str]:
        """Get the most recent emotions from the conversation."""
        return self.dominant_emotions[-count:] if self.dominant_emotions else []
    
    def get_conversation_length(self) -> int:
        """Get the number of turns in this conversation."""
        return len(self.turns)
    
    def has_discussed_topic(self, keywords: List[str]) -> bool:
        """Check if any of the given keywords have been discussed recently."""
        if not keywords or len(self.turns) < 2:
            return False
        
        # Check last 3 turns for topic continuity
        recent_turns = self.turns[-3:]
        for turn in recent_turns:
            user_words = set(turn.user_input.lower().split())
            if any(keyword.lower() in user_words for keyword in keywords):
                return True
        return False