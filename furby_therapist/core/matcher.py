"""
Keyword matcher for categorizing user queries.
"""

import logging
from typing import Dict, List, Tuple, Optional
from .database import ResponseDatabase
from ..models import ResponseCategory, QueryAnalysis


class KeywordMatcher:
    """
    Lightweight keyword matcher that categorizes user queries using string containment
    and weighted scoring for confidence assessment.
    """
    
    def __init__(self, response_database: ResponseDatabase, cycling_mode: bool = False):
        self.database = response_database
        self.categories = response_database.get_all_categories()
        self.cycling_mode = cycling_mode
        # Remove fallback and bicycle from matching categories since fallback is used as default
        # and bicycle category is no longer a special priority case
        self.matching_categories = {k: v for k, v in self.categories.items() if k not in ['fallback', 'bicycle']}
    
    def match_category(self, keywords: List[str]) -> Tuple[str, float]:
        """
        Determine the best response category based on input keywords with error handling.
        
        Args:
            keywords: List of normalized keywords from user input
            
        Returns:
            Tuple of (category_name, confidence_score)
        """
        try:
            # Validate input
            if not keywords or not isinstance(keywords, list):
                logging.debug("Empty or invalid keywords provided to matcher")
                return self.get_fallback_category()
            
            # Filter out invalid keywords
            valid_keywords = [
                kw for kw in keywords 
                if isinstance(kw, str) and len(kw) > 0 and len(kw) < 100
            ]
            
            if not valid_keywords:
                logging.debug("No valid keywords after filtering")
                return self.get_fallback_category()
            
            # Limit keywords to prevent excessive processing
            if len(valid_keywords) > 20:
                logging.warning(f"Too many keywords ({len(valid_keywords)}), truncating to 20")
                valid_keywords = valid_keywords[:20]
            
            # Bicycle keywords are no longer prioritized - they're handled in cycling mode
            
            category_scores = {}
            
            # Calculate scores for each category with error handling
            for category_name, category in self.matching_categories.items():
                try:
                    score = self._calculate_category_score(valid_keywords, category.keywords)
                    if score > 0:
                        category_scores[category_name] = score
                except Exception as e:
                    logging.warning(f"Error calculating score for category {category_name}: {e}")
                    continue
            
            if not category_scores:
                logging.debug("No category matches found, using fallback")
                return self.get_fallback_category()
            
            # Find the category with the highest score
            best_category = max(category_scores.items(), key=lambda x: x[1])
            category_name, confidence = best_category
            
            # Normalize confidence to 0-1 range
            normalized_confidence = min(confidence / len(valid_keywords), 1.0)
            
            logging.debug(f"Best match: {category_name} with confidence {normalized_confidence:.2f}")
            return category_name, normalized_confidence
            
        except Exception as e:
            logging.error(f"Error in match_category: {e}")
            return self.get_fallback_category()
    
    def _calculate_category_score(self, user_keywords: List[str], category_keywords: List[str]) -> float:
        """
        Calculate weighted score for a category based on keyword matches.
        
        Args:
            user_keywords: Keywords extracted from user input
            category_keywords: Keywords associated with the category
            
        Returns:
            Weighted score for the category
        """
        score = 0.0
        
        for user_keyword in user_keywords:
            for category_keyword in category_keywords:
                # Simple string containment check
                if self._keywords_match(user_keyword, category_keyword):
                    # Weight exact matches higher than partial matches
                    if user_keyword == category_keyword:
                        score += 1.0  # Exact match
                    elif user_keyword in category_keyword or category_keyword in user_keyword:
                        score += 0.7  # Partial match
                    else:
                        score += 0.5  # Fuzzy match
        
        return score
    
    def _keywords_match(self, user_keyword: str, category_keyword: str) -> bool:
        """
        Check if two keywords match using string containment.
        
        Args:
            user_keyword: Keyword from user input
            category_keyword: Keyword from category definition
            
        Returns:
            True if keywords match, False otherwise
        """
        # Exact match
        if user_keyword == category_keyword:
            return True
        
        # Containment match - be very strict to avoid false positives
        # Only allow containment for very specific cycling compound words
        cycling_compound_patterns = [
            ('bike', 'biking'), ('bike', 'biker'), ('bike', 'bikes'),
            ('cycle', 'cycling'), ('cycle', 'cyclist'), ('cycle', 'cycles'),
            ('ride', 'riding'), ('ride', 'rider'), ('ride', 'rides'),
            ('wheel', 'wheels'), ('gear', 'gears'), ('chain', 'chains')
        ]
        
        for base, compound in cycling_compound_patterns:
            if (user_keyword == base and category_keyword == compound) or \
               (user_keyword == compound and category_keyword == base):
                return True
        
        # Handle common variations and stemming-like matching
        return self._fuzzy_match(user_keyword, category_keyword)
    
    def _fuzzy_match(self, word1: str, word2: str) -> bool:
        """
        Simple fuzzy matching for common word variations.
        
        Args:
            word1: First word to compare
            word2: Second word to compare
            
        Returns:
            True if words are similar enough to match
        """
        # Don't do fuzzy matching for very short words to avoid false positives
        if len(word1) < 3 or len(word2) < 3:
            return False
            
        # Handle common suffixes (basic stemming-like behavior)
        # Be more restrictive to avoid false matches
        suffix_mappings = [
            ('ing', ''),   # cycling -> cycle
            ('er', ''),    # rider -> ride  
            ('s', ''),     # bikes -> bike
            ('ies', 'y'),  # worries -> worry
        ]
        
        for suffix, replacement in suffix_mappings:
            # Remove suffix from word1 and check match
            if word1.endswith(suffix) and len(word1) > len(suffix):
                stem1 = word1[:-len(suffix)] + replacement
                if len(stem1) >= 3 and (stem1 == word2 or stem1 in word2 or word2 in stem1):
                    return True
            
            # Remove suffix from word2 and check match
            if word2.endswith(suffix) and len(word2) > len(suffix):
                stem2 = word2[:-len(suffix)] + replacement
                if len(stem2) >= 3 and (stem2 == word1 or stem2 in word1 or word1 in stem2):
                    return True
        
        return False
    
    def _check_bicycle_keywords(self, keywords: List[str]) -> float:
        """
        Check for bicycle-related keywords and return a score.
        
        Args:
            keywords: List of keywords to check
            
        Returns:
            Score for bicycle keyword matches (higher = more bicycle-related)
        """
        bicycle_keywords = {
            # Basic cycling terms
            'bike', 'bicycle', 'cycling', 'riding', 'pedal', 'chain', 'wheel', 
            'maintenance', 'cyclist', 'ride', 'biking', 'cycle', 'spoke', 'tire', 
            'brake', 'handlebar', 'saddle', 'frame', 'derailleur', 'cassette',
            'crankset', 'shifter', 'helmet', 'lycra', 'cadence', 'watts', 'strava',
            'peloton', 'gruppetto', 'bonk', 'fred', 'roadie', 'mtb', 'fixie',
            # Alt cycling and gravel culture
            'gravel', 'bikepacking', 'randonneuring', 'xbiking', 'frankenbike', 
            'messenger', 'courier',
            # Gear debates and culture (more specific)
            'clipless', 'flats', 'tubeless', 'psi',
            'vintage', 'retro', 'lugged', 'touring', 'commuter', 'utility',
            # Community and magazine references  
            'quarterly', 'fixed', 'singlespeed', 'conversion', 'track', 'pursuit',
            # Multi-word phrases (with underscores)
            'calling_in_sick', 'bicycle_quarterly', 'alt_cycling', 'gravel_grinding',
            'tire_pressure', 'rigid_mtb', 'mountain_bike', 'bike_messenger',
            'fixed_gear', 'single_speed', 'path_less_pedaled', 'the_radavist',
            'bike_insights', 'endurance_geometry', 'aggressive_geometry',
            # Bike geometry terms
            'geometry', 'reach', 'stack', 'wheelbase', 'chainstay', 'headtube',
            'trail', 'rake', '650b', '700c', 'endurance', 'aggressive', 'slack', 'steep',
            # Alt cycling culture and events
            'radavist', 'porteur', 'constructeur', 'rando', 'audax', 'brevets',
            'permanents', 'fleche', 'pbp', 'tcr', 'monster', 'adventure',
            'grinder', 'retrogrouch', 'luddite', 'weenie'
        }
        
        # More specific cycling terms that need context
        contextual_bicycle_keywords = {
            'gear': ['bike', 'bicycle', 'cycling', 'shift', 'derailleur'],
            'steel': ['bike', 'bicycle', 'frame', 'carbon'],
            'grinding': ['gravel', 'bike', 'cycling'],
            'rigid': ['mtb', 'bike', 'mountain'],
            'carbon': ['bike', 'bicycle', 'frame', 'steel'],
            'pressure': ['tire', 'psi', 'bike', 'bicycle']
        }
        
        score = 0.0
        keywords_lower = [kw.lower() for kw in keywords]  # Handle case sensitivity
        
        for keyword in keywords_lower:
            # Direct matches get full points
            if keyword in bicycle_keywords:
                score += 1.0
            # Check contextual keywords (need supporting context)
            elif keyword in contextual_bicycle_keywords:
                context_words = contextual_bicycle_keywords[keyword]
                if any(ctx_word in keywords_lower for ctx_word in context_words):
                    score += 1.0  # Full score if context is present
                else:
                    score += 0.0  # No score without context
            # Partial matches for compound words - be very selective
            elif len(keyword) > 6 and any(
                (bike_word in keyword and len(bike_word) > 6 and 
                 (keyword.startswith(bike_word) or keyword.endswith(bike_word))) or 
                (keyword in bike_word and len(keyword) > 6 and len(bike_word) > 8 and
                 (bike_word.startswith(keyword) or bike_word.endswith(keyword)))
                for bike_word in bicycle_keywords
            ):
                score += 0.7
            # Check for cycling-related terms that might not be in our main list
            elif self._is_cycling_related(keyword):
                score += 0.5
        
        return score
    
    def _is_cycling_related(self, word: str) -> bool:
        """
        Check if a word is cycling-related using pattern matching.
        
        Args:
            word: Word to check
            
        Returns:
            True if the word appears to be cycling-related
        """
        # Only check for very specific cycling-related patterns
        # to avoid false positives with emotional words
        specific_cycling_patterns = [
            'wheelset', 'tubeless', 'puncture', 'chainring', 'cassette',
            'derailleur', 'groupset', 'crankset', 'headset', 'seatpost',
            'bikepacking', 'randonneuring', 'frankenbike', 'xbiking',
            'gravel', 'grinding', 'messenger', 'courier', 'fixie',
            'singlespeed', 'clipless', 'tubeless', 'pannier', 'dropout',
            'geometry', 'wheelbase', 'chainstay', 'headtube', 'reach',
            'stack', 'trail', 'rake', 'porteur', 'constructeur', 'rando',
            'audax', 'brevets', 'fleche', 'radavist', 'retrogrouch'
        ]
        
        # Check for exact matches or very specific containment
        for pattern in specific_cycling_patterns:
            if word == pattern:
                return True
            # Only allow containment for longer patterns to avoid false matches
            elif len(pattern) > 6 and len(word) > 8 and pattern in word:
                return True
        
        # Check for cycling culture compound words - be very specific
        cycling_compounds = [
            'bike', 'cycle', 'wheel', 'chain', 'gear', 'spoke', 'tire', 'tube'
        ]
        
        # Only match if the word contains cycling terms and is reasonably long
        # AND the cycling term is at the beginning or end of the word (not middle)
        if len(word) > 5:
            for compound in cycling_compounds:
                if len(compound) > 3 and compound in word:
                    # Only match if compound is at start or end of word
                    if word.startswith(compound) or word.endswith(compound):
                        return True
        
        return False
    
    def calculate_confidence(self, matches: Dict[str, float]) -> float:
        """
        Calculate overall confidence score for matches.
        
        Args:
            matches: Dictionary of category names to match scores
            
        Returns:
            Confidence score between 0.0 and 1.0
        """
        if not matches:
            return 0.0
        
        max_score = max(matches.values())
        total_score = sum(matches.values())
        
        # Confidence is based on the strength of the best match relative to total
        if total_score == 0:
            return 0.0
        
        confidence = max_score / total_score
        return min(confidence, 1.0)
    
    def get_fallback_category(self) -> Tuple[str, float]:
        """
        Get the fallback category for unmatched queries.
        
        Returns:
            Tuple of (fallback_category_name, low_confidence_score)
        """
        return 'fallback', 0.1
    
    def analyze_query(self, normalized_text: str, keywords: List[str]) -> QueryAnalysis:
        """
        Perform complete analysis of a user query.
        
        Args:
            normalized_text: Normalized version of the original query
            keywords: Extracted keywords from the query
            
        Returns:
            QueryAnalysis object with categorization results
        """
        category, confidence = self.match_category(keywords)
        
        # Simple emotion detection based on category
        emotion_mapping = {
            'sadness': 'sad',
            'anxiety': 'anxious', 
            'anger': 'angry',
            'happiness': 'happy',
            'confusion': 'confused',
            'loneliness': 'lonely',
            'gratitude': 'grateful',
            'bicycle': 'enthusiastic',
            'general': 'neutral',
            'fallback': 'unknown'
        }
        
        detected_emotion = emotion_mapping.get(category, 'unknown')
        
        return QueryAnalysis(
            original_text=normalized_text,  # Will be set by caller with original text
            normalized_text=normalized_text,
            keywords=keywords,
            detected_emotion=detected_emotion,
            confidence=confidence,
            category=category
        )