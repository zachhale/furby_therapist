"""
Query processor for normalizing and preparing user input.
"""

import re
import string
from typing import List, Optional

from .models import QueryAnalysis


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
        Clean and standardize input text.
        
        Args:
            input_text: Raw user input text
            
        Returns:
            Normalized text (lowercase, no punctuation, cleaned whitespace)
        """
        if not input_text or not input_text.strip():
            return ""
        
        # Convert to lowercase
        text = input_text.lower()
        
        # Remove punctuation except apostrophes (to preserve contractions)
        text = re.sub(r"[^\w\s']", " ", text)
        
        # Handle contractions by removing apostrophes
        text = text.replace("'", "")
        
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def extract_keywords(self, text: str) -> List[str]:
        """
        Identify meaningful keywords from normalized text.
        
        Args:
            text: Normalized text to extract keywords from
            
        Returns:
            List of meaningful keywords (stop words filtered out)
        """
        if not text:
            return []
        
        # Split into words
        words = text.split()
        
        # Filter out stop words and very short words
        keywords = [
            word for word in words 
            if word not in self.STOP_WORDS and len(word) > 2
        ]
        
        # Remove duplicates while preserving order
        seen = set()
        unique_keywords = []
        for keyword in keywords:
            if keyword not in seen:
                seen.add(keyword)
                unique_keywords.append(keyword)
        
        return unique_keywords
    
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
        Complete processing pipeline for user query.
        
        Args:
            input_text: Raw user input
            
        Returns:
            QueryAnalysis object with all extracted information
        """
        # Normalize the text
        normalized = self.normalize_text(input_text)
        
        # Extract keywords
        keywords = self.extract_keywords(normalized)
        
        # Detect emotion
        emotion, confidence = self.detect_emotion(normalized)
        
        return QueryAnalysis(
            original_text=input_text,
            normalized_text=normalized,
            keywords=keywords,
            detected_emotion=emotion,
            confidence=confidence,
            category="general"  # Will be updated by matcher
        )