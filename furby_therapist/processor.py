"""
Query processor for normalizing and preparing user input.
"""

import re
import string
import logging
from typing import List, Optional

from .models import QueryAnalysis
from .error_handler import validate_input


class QueryProcessor:
    """Processes user queries for keyword matching and emotion detection."""
    
    # Keywords that indicate a repeat request
    REPEAT_KEYWORDS = {
        'repeat', 'again', 'say', 'what', 'pardon', 'sorry', 'huh', 'eh',
        'come', 'didnt', 'hear', 'understand', 'catch', 'missed', 'once'
    }
    
    # Common stop words to filter out during keyword extraction
    STOP_WORDS = {
        'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
        'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
        'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
        'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
        'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
        'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
        'while', 'of', 'at', 'by', 'for', 'with', 'through', 'during', 'before', 'after',
        'above', 'below', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
        'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all',
        'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
        'not', 'only', 'own', 'same', 'so', 'than', 'too', 'can', 'will', 'just',
        'should', 'now'
    }
    
    # Emotion keywords for simple emotion detection
    EMOTION_KEYWORDS = {
        'sadness': {
            'sad', 'depressed', 'down', 'blue', 'unhappy', 'miserable', 'crying', 'cry',
            'tears', 'hurt', 'pain', 'heartbroken', 'lonely', 'empty', 'hopeless',
            'devastated', 'grief', 'mourning', 'loss', 'disappointed'
        },
        'anxiety': {
            'anxious', 'worried', 'nervous', 'scared', 'afraid', 'fear', 'panic', 'stress',
            'stressed', 'overwhelmed', 'tense', 'uneasy', 'concerned', 'frightened',
            'terrified', 'paranoid', 'restless', 'agitated', 'jittery', 'apprehensive'
        },
        'anger': {
            'angry', 'mad', 'furious', 'rage', 'irritated', 'annoyed', 'frustrated',
            'pissed', 'livid', 'outraged', 'hostile', 'aggressive', 'bitter', 'resentful',
            'indignant', 'enraged', 'irate', 'incensed', 'infuriated'
        },
        'happiness': {
            'happy', 'joy', 'joyful', 'glad', 'cheerful', 'excited', 'thrilled', 'elated',
            'delighted', 'pleased', 'content', 'satisfied', 'grateful', 'thankful',
            'optimistic', 'positive', 'upbeat', 'ecstatic', 'blissful', 'euphoric'
        },
        'confusion': {
            'confused', 'lost', 'uncertain', 'unsure', 'puzzled', 'bewildered',
            'perplexed', 'baffled', 'unclear', 'mixed up', 'disoriented', 'conflicted',
            'indecisive', 'torn', 'questioning', 'doubtful', 'hesitant'
        },
        'enthusiastic': {
            'bike', 'bicycle', 'cycling', 'riding', 'pedal', 'chain', 'wheel', 'maintenance',
            'cyclist', 'ride', 'biking', 'cycle', 'spoke', 'tire', 'gear', 'brake',
            'handlebar', 'saddle', 'frame', 'love', 'awesome', 'amazing', 'fantastic'
        }
    }
    
    def normalize_text(self, input_text: str) -> str:
        """
        Clean and standardize input text with error handling.
        
        Args:
            input_text: Raw user input text
            
        Returns:
            Normalized text (lowercase, no punctuation, cleaned whitespace)
        """
        try:
            if not input_text or not input_text.strip():
                return ""
            
            # Validate input type
            if not isinstance(input_text, str):
                logging.warning(f"normalize_text received non-string input: {type(input_text)}")
                return ""
            
            # Check for excessively long input
            if len(input_text) > 10000:  # Prevent memory issues
                logging.warning(f"Input text too long: {len(input_text)} characters")
                input_text = input_text[:1000]  # Truncate to reasonable length
            
            # Convert to lowercase
            text = input_text.lower()
            
            # Remove punctuation except apostrophes (to preserve contractions)
            text = re.sub(r"[^\w\s']", " ", text)
            
            # Handle contractions by removing apostrophes
            text = text.replace("'", "")
            
            # Remove extra whitespace and normalize
            text = re.sub(r'\s+', ' ', text).strip()
            
            return text
            
        except Exception as e:
            logging.error(f"Error normalizing text: {e}")
            return ""  # Return empty string on error
    
    def extract_keywords(self, text: str) -> List[str]:
        """
        Identify meaningful keywords from normalized text with error handling.
        
        Args:
            text: Normalized text to extract keywords from
            
        Returns:
            List of meaningful keywords (stop words filtered out)
        """
        try:
            if not text or not isinstance(text, str):
                return []
            
            # Check for cycling-specific multi-word phrases first
            cycling_phrases = self._extract_cycling_phrases(text)
            
            # Split into words with error handling
            words = text.split()
            
            # Limit number of words to prevent excessive processing
            if len(words) > 100:
                logging.warning(f"Too many words in input: {len(words)}, truncating")
                words = words[:100]
            
            # Filter out stop words and very short words
            keywords = []
            for word in words:
                if (word not in self.STOP_WORDS and 
                    len(word) > 2 and 
                    len(word) < 50 and  # Prevent extremely long words
                    word.isalnum()):  # Only alphanumeric words
                    keywords.append(word)
            
            # Add cycling phrases to keywords
            keywords.extend(cycling_phrases)
            
            # Remove duplicates while preserving order
            seen = set()
            unique_keywords = []
            for keyword in keywords:
                if keyword not in seen:
                    seen.add(keyword)
                    unique_keywords.append(keyword)
            
            # Limit number of keywords to prevent excessive processing
            if len(unique_keywords) > 20:
                unique_keywords = unique_keywords[:20]
            
            return unique_keywords
            
        except Exception as e:
            logging.error(f"Error extracting keywords: {e}")
            return []
    
    def _extract_cycling_phrases(self, text: str) -> List[str]:
        """
        Extract cycling-specific multi-word phrases from text.
        
        Args:
            text: Text to search for cycling phrases
            
        Returns:
            List of cycling phrases found in the text
        """
        cycling_phrases = [
            'calling in sick',
            'bicycle quarterly',
            'alt cycling',
            'gravel grinding',
            'tire pressure',
            'rigid mtb',
            'mountain bike',
            'bike messenger',
            'fixed gear',
            'single speed',
            'path less pedaled',
            'the radavist',
            'bike insights',
            'endurance geometry',
            'aggressive geometry',
            'touring geometry',
            'monster cross',
            'all road',
            'gravel grinder',
            'adventure bike',
            'bb drop',
            'head tube',
            'chain stay',
            'reach stack',
            'weight weenie',
            'dentist bike',
            'fred sled'
        ]
        
        found_phrases = []
        text_lower = text.lower()
        
        for phrase in cycling_phrases:
            if phrase in text_lower:
                # Add the phrase as a single keyword (replace spaces with underscores)
                found_phrases.append(phrase.replace(' ', '_'))
        
        return found_phrases
    
    def detect_emotion(self, text: str) -> tuple[str, float]:
        """
        Simple emotion detection based on keyword presence.
        
        Args:
            text: Normalized text to analyze for emotions
            
        Returns:
            Tuple of (emotion_name, confidence_score)
        """
        if not text:
            return "neutral", 0.0
        
        words = set(text.split())
        emotion_scores = {}
        
        # Calculate scores for each emotion based on keyword matches
        for emotion, keywords in self.EMOTION_KEYWORDS.items():
            matches = words.intersection(keywords)
            if matches:
                # Score based on number of matches and total words
                score = len(matches) / len(words) if words else 0
                emotion_scores[emotion] = score
        
        if not emotion_scores:
            return "neutral", 0.0
        
        # Return emotion with highest score
        best_emotion = max(emotion_scores.items(), key=lambda x: x[1])
        return best_emotion[0], best_emotion[1]
    
    def is_repeat_request(self, text: str) -> bool:
        """
        Detect if the user is asking for a repeat of the previous response.
        
        Args:
            text: Text to analyze (will be normalized internally)
            
        Returns:
            True if this appears to be a repeat request
        """
        if not text:
            return False
        
        # Normalize the text first
        normalized_text = self.normalize_text(text)
        if not normalized_text:
            return False
        
        words = set(normalized_text.split())
        
        # Check for repeat keywords
        repeat_matches = words.intersection(self.REPEAT_KEYWORDS)
        
        # Common repeat patterns
        repeat_patterns = [
            'say again', 'what did you say', 'repeat that', 'come again',
            'didnt hear', 'didnt understand', 'didnt catch', 'say that again',
            'what was that', 'pardon me', 'excuse me', 'sorry what'
        ]
        
        # Check for exact phrase matches
        for pattern in repeat_patterns:
            if pattern in normalized_text:
                return True
        
        # If we have repeat keywords and the query is short (likely just asking for repeat)
        if repeat_matches and len(words) <= 4:
            return True
        
        # Special case for very short queries that are likely repeat requests
        if len(words) <= 2 and any(word in self.REPEAT_KEYWORDS for word in words):
            return True
        
        return False
    
    def process_query(self, input_text: str) -> QueryAnalysis:
        """
        Complete processing pipeline for user query with comprehensive error handling.
        
        Args:
            input_text: Raw user input
            
        Returns:
            QueryAnalysis object with all extracted information
        """
        try:
            # Validate input first
            is_valid, validation_error = validate_input(input_text, max_length=1000)
            if not is_valid:
                logging.warning(f"Query validation failed: {validation_error}")
                # Return minimal analysis for invalid input
                return QueryAnalysis(
                    original_text=input_text or "",
                    normalized_text="",
                    keywords=[],
                    detected_emotion="neutral",
                    confidence=0.0,
                    category="fallback"
                )
            
            # Normalize the text
            normalized = self.normalize_text(input_text)
            
            # Extract keywords
            keywords = self.extract_keywords(normalized)
            
            # Detect emotion
            emotion, confidence = self.detect_emotion(normalized)
            
            # Log processing results for debugging
            logging.debug(f"Query processed: emotion={emotion}, keywords={len(keywords)}, confidence={confidence:.2f}")
            
            return QueryAnalysis(
                original_text=input_text,
                normalized_text=normalized,
                keywords=keywords,
                detected_emotion=emotion,
                confidence=confidence,
                category="general"  # Will be updated by matcher
            )
            
        except Exception as e:
            logging.error(f"Error processing query: {e}")
            # Return safe fallback analysis
            return QueryAnalysis(
                original_text=input_text or "",
                normalized_text="",
                keywords=[],
                detected_emotion="neutral",
                confidence=0.0,
                category="fallback"
            )