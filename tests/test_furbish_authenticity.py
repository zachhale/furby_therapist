"""
Unit tests for Furbish phrase authenticity and proper formatting.

Tests validate that all Furbish phrases used in the application are authentic
according to the original 1998 Furby documentation.
"""

import unittest
import json
import sys
import os

# Add the furby_therapist directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'furby_therapist'))

from furbish_reference import (
    AUTHENTIC_FURBISH,
    THERAPEUTIC_FURBISH,
    validate_furbish_phrase,
    get_authentic_therapeutic_phrases
)


class TestFurbishAuthenticity(unittest.TestCase):
    """Test suite for Furbish phrase authenticity validation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.responses_file = os.path.join(
            os.path.dirname(__file__), '..', 'furby_therapist', 'responses.json'
        )
        
        # Load responses data
        with open(self.responses_file, 'r', encoding='utf-8') as f:
            self.responses_data = json.load(f)
    
    def test_authentic_furbish_dictionary_completeness(self):
        """Test that the authentic Furbish dictionary contains expected words."""
        expected_words = [
            'dah', 'boo', 'kah', 'u-nye', 'way-loh', 'may-may', 'a-loh',
            'doo-moh', 'loo-loo', 'koh-koh', 'wee-tah', 'ooh-lah', 'eee-day',
            'boh-bay', 'noo-loo', 'dee-doh', 'way-way', 'wah'
        ]
        
        for word in expected_words:
            self.assertIn(word, AUTHENTIC_FURBISH, 
                         f"Expected authentic word '{word}' not found in dictionary")
    
    def test_therapeutic_phrases_authenticity(self):
        """Test that all therapeutic phrases use authentic Furbish words."""
        for phrase, translation in THERAPEUTIC_FURBISH.items():
            is_valid, corrected, explanation = validate_furbish_phrase(phrase)
            self.assertTrue(is_valid, 
                           f"Therapeutic phrase '{phrase}' is not authentic: {explanation}")
    
    def test_responses_json_furbish_authenticity(self):
        """Test that all Furbish phrases in responses.json are authentic."""
        categories = self.responses_data.get('categories', {})
        
        for category_name, category_data in categories.items():
            furbish_phrases = category_data.get('furbish_phrases', [])
            
            for phrase_pair in furbish_phrases:
                self.assertEqual(len(phrase_pair), 2, 
                               f"Invalid phrase format in {category_name}: {phrase_pair}")
                
                furbish_phrase, english_translation = phrase_pair
                is_valid, corrected, explanation = validate_furbish_phrase(furbish_phrase)
                
                self.assertTrue(is_valid, 
                               f"Non-authentic phrase in {category_name}: '{furbish_phrase}' - {explanation}")
    
    def test_furbish_phrase_formatting(self):
        """Test that Furbish phrases follow proper formatting rules."""
        categories = self.responses_data.get('categories', {})
        
        for category_name, category_data in categories.items():
            furbish_phrases = category_data.get('furbish_phrases', [])
            
            for phrase_pair in furbish_phrases:
                furbish_phrase, english_translation = phrase_pair
                
                # Test hyphenation (multi-word phrases should use hyphens)
                if len(furbish_phrase.split('-')) > 1:
                    self.assertNotIn(' ', furbish_phrase, 
                                   f"Phrase should use hyphens, not spaces: '{furbish_phrase}'")
                
                # Test lowercase (all Furbish should be lowercase)
                self.assertEqual(furbish_phrase, furbish_phrase.lower(), 
                               f"Furbish phrase should be lowercase: '{furbish_phrase}'")
                
                # Test no invalid characters
                valid_chars = set('abcdefghijklmnopqrstuvwxyz-')
                phrase_chars = set(furbish_phrase)
                invalid_chars = phrase_chars - valid_chars
                self.assertEqual(len(invalid_chars), 0, 
                               f"Invalid characters in phrase '{furbish_phrase}': {invalid_chars}")
    
    def test_english_translations_accuracy(self):
        """Test that English translations are accurate for authentic phrases."""
        test_cases = [
            ('kah-may-may-u-nye', 'me love you'),
            ('u-nye-noo-loo', 'you happy'),
            ('koh-koh', 'sleep/calm'),
            ('boh-bay', 'hug'),
            ('way-way-dee-doh', 'play big'),
            ('dah-way-loh', 'yes again')
        ]
        
        for furbish, expected_english in test_cases:
            # Find this phrase in responses.json
            found = False
            categories = self.responses_data.get('categories', {})
            
            for category_data in categories.values():
                furbish_phrases = category_data.get('furbish_phrases', [])
                for phrase_pair in furbish_phrases:
                    if phrase_pair[0] == furbish:
                        actual_english = phrase_pair[1]
                        self.assertEqual(actual_english, expected_english,
                                       f"Translation mismatch for '{furbish}': "
                                       f"expected '{expected_english}', got '{actual_english}'")
                        found = True
                        break
                if found:
                    break
    
    def test_no_invented_words(self):
        """Test that no invented or non-authentic words are used."""
        # List of words that were previously used but are not authentic
        non_authentic_words = [
            'wheel', 'pedal', 'cycle', 'bike', 'chain', 'spoke'
        ]
        
        categories = self.responses_data.get('categories', {})
        
        for category_name, category_data in categories.items():
            furbish_phrases = category_data.get('furbish_phrases', [])
            
            for phrase_pair in furbish_phrases:
                furbish_phrase = phrase_pair[0]
                words = furbish_phrase.split('-')
                
                for word in words:
                    self.assertNotIn(word, non_authentic_words,
                                   f"Non-authentic word '{word}' found in phrase '{furbish_phrase}' "
                                   f"in category '{category_name}'")
    
    def test_bicycle_themed_phrases_use_authentic_words(self):
        """Test that bicycle-themed phrases only use authentic Furbish words."""
        bicycle_category = self.responses_data.get('categories', {}).get('bicycle', {})
        furbish_phrases = bicycle_category.get('furbish_phrases', [])
        
        # All bicycle phrases should be validated as authentic
        for phrase_pair in furbish_phrases:
            furbish_phrase = phrase_pair[0]
            is_valid, corrected, explanation = validate_furbish_phrase(furbish_phrase)
            self.assertTrue(is_valid,
                           f"Bicycle phrase '{furbish_phrase}' is not authentic: {explanation}")
    
    def test_phrase_diversity_across_categories(self):
        """Test that different categories use diverse Furbish phrases."""
        all_phrases = []
        categories = self.responses_data.get('categories', {})
        
        for category_name, category_data in categories.items():
            furbish_phrases = category_data.get('furbish_phrases', [])
            category_phrases = [phrase[0] for phrase in furbish_phrases]
            all_phrases.extend(category_phrases)
        
        # Should have some variety (not all the same phrase)
        unique_phrases = set(all_phrases)
        self.assertGreater(len(unique_phrases), 1, 
                          "Should have more than one unique Furbish phrase across all categories")
    
    def test_validation_function_accuracy(self):
        """Test that the validation function correctly identifies authentic phrases."""
        # Test authentic phrases
        authentic_test_cases = [
            'kah-may-may-u-nye',
            'u-nye-noo-loo', 
            'koh-koh',
            'boh-bay',
            'way-way-dee-doh'
        ]
        
        for phrase in authentic_test_cases:
            is_valid, corrected, explanation = validate_furbish_phrase(phrase)
            self.assertTrue(is_valid, f"Authentic phrase '{phrase}' marked as invalid: {explanation}")
        
        # Test non-authentic phrases
        non_authentic_test_cases = [
            'dah wheel-loh',  # contains non-authentic 'wheel'
            'kah pedal-may',  # contains non-authentic 'pedal'
            'fake-word-here'  # completely invented
        ]
        
        for phrase in non_authentic_test_cases:
            is_valid, corrected, explanation = validate_furbish_phrase(phrase)
            self.assertFalse(is_valid, f"Non-authentic phrase '{phrase}' marked as valid")


class TestFurbishReference(unittest.TestCase):
    """Test suite for the Furbish reference module functionality."""
    
    def test_get_authentic_therapeutic_phrases(self):
        """Test that get_authentic_therapeutic_phrases returns valid data."""
        phrases = get_authentic_therapeutic_phrases()
        
        self.assertIsInstance(phrases, dict)
        self.assertGreater(len(phrases), 0)
        
        # All keys should be valid Furbish phrases
        for phrase, translation in phrases.items():
            self.assertIsInstance(phrase, str)
            self.assertIsInstance(translation, str)
            self.assertGreater(len(phrase), 0)
            self.assertGreater(len(translation), 0)
    
    def test_validate_furbish_phrase_return_format(self):
        """Test that validate_furbish_phrase returns the correct format."""
        result = validate_furbish_phrase('kah-may-may-u-nye')
        
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 3)
        
        is_valid, corrected, explanation = result
        self.assertIsInstance(is_valid, bool)
        self.assertIsInstance(corrected, str)
        self.assertIsInstance(explanation, str)


if __name__ == '__main__':
    unittest.main()