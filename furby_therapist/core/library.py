"""
FurbyTherapist Library - A reusable library for generating Furby-style therapeutic responses.

This library provides a clean interface for integrating Furby therapeutic responses
into any application, separate from CLI-specific functionality.
"""

import logging
from typing import Dict, List, Optional, Tuple
from pathlib import Path

from .database import ResponseDatabase
from .processor import QueryProcessor
from .matcher import KeywordMatcher
from .responses import ResponseEngine
from ..models import QueryAnalysis, FurbyResponse, ConversationSession, ResponseCategory
from .error_handler import FurbyErrorHandler, validate_input


class FurbyTherapist:
    """
    Main library class for Furby therapeutic response generation.
    
    This class encapsulates all the core functionality for processing queries
    and generating therapeutic responses in Furby style, with optional cycling mode.
    
    Can be used in both stateful mode (maintains conversation context) and 
    stateless mode (single query processing).
    """
    
    def __init__(self, cycling_mode: bool = False, maintain_session: bool = True):
        """
        Initialize the FurbyTherapist library.
        
        Args:
            cycling_mode: Enable cycling-themed responses and metaphors
            maintain_session: Whether to maintain conversation history (stateful mode)
        """
        self.cycling_mode = cycling_mode
        self.maintain_session = maintain_session
        
        # Initialize error handler
        self.error_handler = FurbyErrorHandler()
        
        try:
            # Initialize core components
            self.database = ResponseDatabase()
            self.processor = QueryProcessor()
            self.matcher = KeywordMatcher(self.database, cycling_mode=cycling_mode)
            self.response_engine = ResponseEngine(cycling_mode=cycling_mode)
            
            # Initialize conversation session if stateful mode
            self.conversation = ConversationSession() if maintain_session else None
            
            # Track consecutive empty inputs for better UX
            self.empty_input_count = 0
            
            # Log successful initialization
            mode_info = "cycling mode" if cycling_mode else "standard mode"
            session_info = "stateful" if maintain_session else "stateless"
            self.error_handler.logger.info(
                f"FurbyTherapist library initialized in {mode_info}, {session_info} mode"
            )
            
        except Exception as e:
            error_msg = self.error_handler.log_error(e, "library initialization")
            raise RuntimeError(f"Failed to initialize FurbyTherapist library: {error_msg}")
    
    def process_query(self, query: str) -> FurbyResponse:
        """
        Process a single query and return a Furby therapeutic response.
        
        Args:
            query: User's input text
            
        Returns:
            FurbyResponse object containing the therapeutic response
            
        Raises:
            ValueError: If query is invalid
            RuntimeError: If processing fails
        """
        try:
            # Check memory usage before processing
            memory_warning = self.error_handler.check_memory_usage()
            if memory_warning and "critical" in memory_warning.lower():
                self.error_handler.cleanup_resources()
                return self._create_memory_warning_response(memory_warning)
            
            # Validate input
            is_valid, validation_error = validate_input(query, max_length=1000)
            if not is_valid:
                self.error_handler.logger.warning(f"Input validation failed: {validation_error}")
                raise ValueError(validation_error)
            
            # Handle empty input
            if not query or not query.strip():
                return self._handle_empty_input()
            
            # Reset empty input counter on valid input
            self.empty_input_count = 0
            
            # Log query processing start
            self.error_handler.logger.debug(f"Processing query: {query[:50]}...")
            
            # Check if this is a repeat request
            if self.processor.is_repeat_request(query):
                self.error_handler.logger.debug("Repeat request detected")
                if self.response_engine.has_cached_response():
                    repeat_response = self.response_engine.get_repeat_response()
                    if repeat_response:
                        return repeat_response
                
                # No cached response available
                return self._create_no_repeat_response()
            
            # Step 1: Process the query (normalize text, extract keywords, detect emotion)
            analysis = self.processor.process_query(query)
            self.error_handler.logger.debug(
                f"Query analysis: emotion={analysis.detected_emotion}, keywords={analysis.keywords[:3]}"
            )
            
            # Step 2: Use conversation context to enhance matching if in stateful mode
            if self.maintain_session and self.conversation:
                analysis = self._enhance_with_conversation_context(analysis)
            
            # Step 3: Match keywords to determine response category
            category, confidence = self.matcher.match_category(analysis.keywords)
            self.error_handler.logger.debug(f"Matched category: {category} (confidence: {confidence:.2f})")
            
            # Update analysis with matched category
            analysis.category = category
            analysis.confidence = confidence
            
            # Step 4: Generate Furby-style therapeutic response
            furby_response = self.response_engine.get_response(category, analysis.detected_emotion)
            
            # Step 5: Add conversation turn to history if in stateful mode
            if self.maintain_session and self.conversation:
                self.conversation.add_turn(
                    user_input=query,
                    user_emotion=analysis.detected_emotion,
                    furby_response=furby_response.formatted_output,
                    response_category=category
                )
            
            # Step 6: Check memory usage after processing
            memory_warning = self.error_handler.check_memory_usage()
            if memory_warning:
                self.error_handler.logger.warning("Memory usage high after query processing")
            
            self.error_handler.logger.debug("Query processed successfully")
            return furby_response
            
        except ValueError:
            # Re-raise validation errors
            raise
        except Exception as e:
            # Handle unexpected errors
            error_msg = self.error_handler.log_error(e, "query processing", query)
            raise RuntimeError(f"Failed to process query: {error_msg}")
    
    def _handle_empty_input(self) -> FurbyResponse:
        """Handle empty input with contextual responses."""
        if self.empty_input_count == 0:
            message = "*gentle chirp* Furby is listening! Tell me what's on your mind! *encouraging beep*"
        elif self.empty_input_count == 1:
            message = "*patient purr* Take your time! Furby is here when you're ready to share! *supportive chirp*"
        else:
            message = "*understanding beep* Sometimes it's hard to find words. That's okay! Furby understands! *gentle purr*"
        
        self.empty_input_count += 1
        self.error_handler.logger.debug(f"Empty input handled, count: {self.empty_input_count}")
        
        return FurbyResponse(
            base_message=message,
            furby_sounds=["*gentle chirp*", "*encouraging beep*"],
            furbish_phrase=None,
            formatted_output=message,
            clean_version="Furby is listening! Tell me what's on your mind!"
        )
    
    def _create_memory_warning_response(self, warning: str) -> FurbyResponse:
        """Create a response for memory warnings."""
        message = f"*gentle beep* Furby needs to take a little break to organize thoughts! *supportive chirp*\n\n{warning}"
        
        return FurbyResponse(
            base_message=message,
            furby_sounds=["*gentle beep*", "*supportive chirp*"],
            furbish_phrase=None,
            formatted_output=message,
            clean_version="Furby needs to take a little break to organize thoughts!"
        )
    
    def _create_no_repeat_response(self) -> FurbyResponse:
        """Create a response when no cached response is available for repeat."""
        message = "*confused chirp* Ooh! Furby doesn't remember what to repeat! Ask me something new! *gentle beep*"
        
        return FurbyResponse(
            base_message=message,
            furby_sounds=["*confused chirp*", "*gentle beep*"],
            furbish_phrase=None,
            formatted_output=message,
            clean_version="Furby doesn't remember what to repeat! Ask me something new!"
        )
    
    def _enhance_with_conversation_context(self, analysis: QueryAnalysis) -> QueryAnalysis:
        """
        Enhance query analysis with conversation history context.
        
        Args:
            analysis: Initial query analysis
            
        Returns:
            Enhanced analysis with conversation context
        """
        if not self.conversation:
            return analysis
        
        # Check if we've been discussing similar topics
        if self.conversation.has_discussed_topic(analysis.keywords):
            # Boost confidence for continuing conversations
            analysis.confidence = min(1.0, analysis.confidence + 0.2)
        
        # Consider recent emotional context
        recent_emotions = self.conversation.get_recent_emotions()
        if recent_emotions and analysis.detected_emotion == "neutral":
            # If current query is neutral but recent emotions exist, use most recent
            analysis.detected_emotion = recent_emotions[-1]
            analysis.confidence = max(0.3, analysis.confidence)
        
        return analysis
    
    def get_available_categories(self) -> List[str]:
        """
        Get list of available response categories.
        
        Returns:
            List of category names
        """
        return self.response_engine.get_available_categories()
    
    def get_category_info(self, category: str) -> Optional[ResponseCategory]:
        """
        Get information about a specific response category.
        
        Args:
            category: Name of the category to get info for
            
        Returns:
            ResponseCategory object or None if not found
        """
        return self.response_engine.get_category_info(category)
    
    def get_conversation_history(self) -> Optional[ConversationSession]:
        """
        Get the current conversation session (if in stateful mode).
        
        Returns:
            ConversationSession object or None if in stateless mode
        """
        return self.conversation if self.maintain_session else None
    
    def clear_conversation_history(self) -> None:
        """Clear conversation history (only works in stateful mode)."""
        if self.maintain_session:
            self.conversation = ConversationSession()
            self.empty_input_count = 0
            self.error_handler.logger.info("Conversation history cleared")
    
    def get_good_morning_greeting(self) -> str:
        """
        Get a good morning greeting with authentic Furbish.
        
        Returns:
            Formatted good morning message
        """
        return self.response_engine.get_good_morning_greeting()
    
    def get_good_night_greeting(self) -> str:
        """
        Get a good night greeting with authentic Furbish.
        
        Returns:
            Formatted good night message
        """
        return self.response_engine.get_good_night_greeting()
    
    def has_cached_response(self) -> bool:
        """
        Check if there's a cached response available for repeat.
        
        Returns:
            True if a cached response is available
        """
        return self.response_engine.has_cached_response()
    
    def get_repeat_response(self) -> Optional[FurbyResponse]:
        """
        Get a repeat of the last response in a cleaner format.
        
        Returns:
            FurbyResponse with clean version, or None if no previous response
        """
        return self.response_engine.get_repeat_response()
    
    def clear_response_cache(self) -> None:
        """Clear the cached response."""
        self.response_engine.clear_cache()
    
    def is_cycling_mode(self) -> bool:
        """
        Check if cycling mode is enabled.
        
        Returns:
            True if cycling mode is active
        """
        return self.cycling_mode
    
    def is_stateful(self) -> bool:
        """
        Check if the library is in stateful mode (maintains conversation context).
        
        Returns:
            True if maintaining conversation session
        """
        return self.maintain_session
    
    def get_session_stats(self) -> Dict[str, any]:
        """
        Get statistics about the current session (if in stateful mode).
        
        Returns:
            Dictionary with session statistics
        """
        if not self.maintain_session or not self.conversation:
            return {"stateful_mode": False}
        
        return {
            "stateful_mode": True,
            "conversation_length": self.conversation.get_conversation_length(),
            "recent_emotions": self.conversation.get_recent_emotions(),
            "session_start": self.conversation.session_start,
            "cycling_mode": self.cycling_mode
        }
    
    def cleanup(self) -> None:
        """Clean up resources and perform any necessary cleanup."""
        try:
            self.error_handler.cleanup_resources()
            self.error_handler.logger.info("FurbyTherapist library cleanup completed")
        except Exception as e:
            self.error_handler.logger.warning(f"Error during cleanup: {e}")


# Convenience functions for simple usage

def create_furby_therapist(cycling_mode: bool = False, stateful: bool = True) -> FurbyTherapist:
    """
    Convenience function to create a FurbyTherapist instance.
    
    Args:
        cycling_mode: Enable cycling-themed responses
        stateful: Maintain conversation context
        
    Returns:
        Configured FurbyTherapist instance
    """
    return FurbyTherapist(cycling_mode=cycling_mode, maintain_session=stateful)


def process_single_query(query: str, cycling_mode: bool = False) -> FurbyResponse:
    """
    Convenience function for processing a single query without maintaining state.
    
    Args:
        query: User's input text
        cycling_mode: Enable cycling-themed responses
        
    Returns:
        FurbyResponse object
        
    Raises:
        ValueError: If query is invalid
        RuntimeError: If processing fails
    """
    therapist = FurbyTherapist(cycling_mode=cycling_mode, maintain_session=False)
    try:
        return therapist.process_query(query)
    finally:
        therapist.cleanup()