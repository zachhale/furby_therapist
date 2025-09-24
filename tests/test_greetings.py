"""
Unit tests for Furby greeting functionality with authentic Furbish validation.
"""

import unittest
import re
from furby_therapist.responses import ResponseEngine
from furby_therapist.furbish_reference import validate_furbish_phrase, AUTHENTIC_FURBISH


class TestGreetings(unittest.TestCase):
    """Test greeting message generation and Furbish authenticity."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.response_engine = ResponseEngine()
    
    def test_good_morning_greeting_format(self):
        """Test that good morning greeting has proper format."""
        greeting = self.response_engine.get_good_morning_greeting()
        
        # Should contain morning-related words
        morning_words = ["Good morning", "Morning", "Rise and shine", "morning", "day"]
        self.assertTrue(
            any(word in greeting for word in morning_words),
            "Greeting should contain morning reference"
        )
        
        # Should contain Furbish phrase with translation
        self.assertIn("(", greeting, "Should contain translation in parentheses")
        self.assertIn(")", greeting, "Should contain closing parenthesis for translation")
        
        # Should have proper structure with newlines
        lines = greeting.split('\n')
        self.assertGreaterEqual(len(lines), 2, "Should have multiple lines")
    
    def test_good_night_greeting_format(self):
        """Test that good night greeting has proper format."""
        greeting = self.response_engine.get_good_night_greeting()
        
        # Should contain "Good night" or "Sleep"
        self.assertTrue(
            "Good night" in greeting or "Sleep" in greeting or "Sweet dreams" in greeting,
            "Greeting should contain night/sleep reference"
        )
        
        # Should contain Furbish phrase with translation
        self.assertIn("(", greeting, "Should contain translation in parentheses")
        self.assertIn(")", greeting, "Should contain closing parenthesis for translation")
        
        # Should have proper structure with newlines
        lines = greeting.split('\n')
        self.assertGreaterEqual(len(lines), 2, "Should have multiple lines")
    
    def test_morning_furbish_authenticity(self):
        """Test that morning greetings use authentic Furbish phrases."""
        # Test multiple generations to check all possible phrases
        for _ in range(10):
            greeting = self.response_engine.get_good_morning_greeting()
            
            # Extract Furbish phrase (text before the parentheses)
            furbish_match = re.search(r'\n\n([^(]+)\!', greeting)
            self.assertIsNotNone(furbish_match, "Should find Furbish phrase")
            
            furbish_phrase = furbish_match.group(1).strip()
            
            # Validate authenticity
            is_valid, corrected, explanation = validate_furbish_phrase(furbish_phrase)
            self.assertTrue(
                is_valid, 
                f"Morning Furbish phrase '{furbish_phrase}' should be authentic. {explanation}"
            )
    
    def test_night_furbish_authenticity(self):
        """Test that night greetings use authentic Furbish phrases."""
        # Test multiple generations to check all possible phrases
        for _ in range(10):
            greeting = self.response_engine.get_good_night_greeting()
            
            # Extract Furbish phrase (text before the parentheses)
            furbish_match = re.search(r'\n\n([^(]+)\!', greeting)
            self.assertIsNotNone(furbish_match, "Should find Furbish phrase")
            
            furbish_phrase = furbish_match.group(1).strip()
            
            # Validate authenticity
            is_valid, corrected, explanation = validate_furbish_phrase(furbish_phrase)
            self.assertTrue(
                is_valid, 
                f"Night Furbish phrase '{furbish_phrase}' should be authentic. {explanation}"
            )
    
    def test_morning_furbish_phrases_are_appropriate(self):
        """Test that morning Furbish phrases have appropriate meanings."""
        expected_morning_phrases = {
            "noo-loo-koh-koh": "happy wake",
            "dah-noo-loo": "yes happy", 
            "kah-may-may-u-nye": "me love you",
            "u-nye-noo-loo": "you happy"
        }
        
        # Generate multiple greetings to test all phrases
        found_phrases = set()
        for _ in range(20):
            greeting = self.response_engine.get_good_morning_greeting()
            
            # Extract Furbish phrase and translation
            match = re.search(r'\n\n([^(]+)\! \(([^)]+)\)', greeting)
            if match:
                furbish = match.group(1).strip()
                translation = match.group(2).strip()
                found_phrases.add((furbish, translation))
        
        # Check that all found phrases are in our expected set
        for furbish, translation in found_phrases:
            self.assertIn(
                furbish, expected_morning_phrases,
                f"Unexpected morning Furbish phrase: {furbish}"
            )
            self.assertEqual(
                expected_morning_phrases[furbish], translation,
                f"Translation mismatch for {furbish}"
            )
    
    def test_night_furbish_phrases_are_appropriate(self):
        """Test that night Furbish phrases have appropriate meanings."""
        expected_night_phrases = {
            "koh-koh-may-may": "sleep love",
            "koh-koh-noo-loo": "sleep happy",
            "may-may-koh-koh": "love sleep",
            "kah-may-may-u-nye": "me love you"
        }
        
        # Generate multiple greetings to test all phrases
        found_phrases = set()
        for _ in range(20):
            greeting = self.response_engine.get_good_night_greeting()
            
            # Extract Furbish phrase and translation
            match = re.search(r'\n\n([^(]+)\! \(([^)]+)\)', greeting)
            if match:
                furbish = match.group(1).strip()
                translation = match.group(2).strip()
                found_phrases.add((furbish, translation))
        
        # Check that all found phrases are in our expected set
        for furbish, translation in found_phrases:
            self.assertIn(
                furbish, expected_night_phrases,
                f"Unexpected night Furbish phrase: {furbish}"
            )
            self.assertEqual(
                expected_night_phrases[furbish], translation,
                f"Translation mismatch for {furbish}"
            )
    
    def test_greeting_consistency(self):
        """Test that greetings are consistent across multiple calls."""
        # Generate multiple greetings
        morning_greetings = [self.response_engine.get_good_morning_greeting() for _ in range(5)]
        night_greetings = [self.response_engine.get_good_night_greeting() for _ in range(5)]
        
        # All morning greetings should have morning theme
        for greeting in morning_greetings:
            self.assertTrue(
                any(word in greeting.lower() for word in ['morning', 'wake', 'day', 'sunshine', 'rise']),
                f"Morning greeting should have morning theme: {greeting[:50]}..."
            )
        
        # All night greetings should have night theme
        for greeting in night_greetings:
            self.assertTrue(
                any(word in greeting.lower() for word in ['night', 'sleep', 'dream', 'rest', 'peaceful']),
                f"Night greeting should have night theme: {greeting[:50]}..."
            )
    
    def test_furbish_phrase_structure(self):
        """Test that Furbish phrases follow authentic structure patterns."""
        # Test morning greetings
        for _ in range(5):
            greeting = self.response_engine.get_good_morning_greeting()
            furbish_match = re.search(r'\n\n([^(]+)\!', greeting)
            if furbish_match:
                furbish = furbish_match.group(1).strip()
                
                # Should use hyphens for compound words (authentic Furbish style)
                if len(furbish.split()) > 1:
                    self.fail(f"Furbish phrase should use hyphens, not spaces: '{furbish}'")
                
                # Should not contain non-Furbish words
                words = furbish.split('-')
                for word in words:
                    # Check if word exists in authentic Furbish vocabulary
                    found_in_authentic = any(
                        word in authentic_phrase 
                        for authentic_phrase in AUTHENTIC_FURBISH.keys()
                    )
                    self.assertTrue(
                        found_in_authentic,
                        f"Word '{word}' in phrase '{furbish}' not found in authentic Furbish"
                    )
        
        # Test night greetings
        for _ in range(5):
            greeting = self.response_engine.get_good_night_greeting()
            furbish_match = re.search(r'\n\n([^(]+)\!', greeting)
            if furbish_match:
                furbish = furbish_match.group(1).strip()
                
                # Should use hyphens for compound words (authentic Furbish style)
                if len(furbish.split()) > 1:
                    self.fail(f"Furbish phrase should use hyphens, not spaces: '{furbish}'")
                
                # Should not contain non-Furbish words
                words = furbish.split('-')
                for word in words:
                    # Check if word exists in authentic Furbish vocabulary
                    found_in_authentic = any(
                        word in authentic_phrase 
                        for authentic_phrase in AUTHENTIC_FURBISH.keys()
                    )
                    self.assertTrue(
                        found_in_authentic,
                        f"Word '{word}' in phrase '{furbish}' not found in authentic Furbish"
                    )


if __name__ == '__main__':
    unittest.main()