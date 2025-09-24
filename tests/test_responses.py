"""
Unit tests for the Furby response engine.
"""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from furby_therapist.responses import ResponseEngine
from furby_therapist.models import FurbyResponse, ResponseCategory


class TestResponseEngine(unittest.TestCase):
    """Test cases for the ResponseEngine class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a minimal test responses file
        self.test_responses = {
            "schema_version": "1.0",
            "categories": {
                "test_category": {
                    "keywords": ["test", "sample"],
                    "responses": [
                        "Test response 1! *chirp*",
                        "Test response 2! *purr*"
                    ],
                    "furby_sounds": ["*chirp*", "*purr*", "ooh!"],
                    "furbish_phrases": [
                        ["Dah test", "test phrase"],
                        ["Kah sample", "sample phrase"]
                    ]
                },
                "fallback": {
                    "keywords": [],
                    "responses": [
                        "Fallback response! *gentle chirp*"
                    ],
                    "furby_sounds": ["*chirp*"],
                    "furbish_phrases": [
                        ["Dah koh-koh", "it's okay"]
                    ]
                }
            }
        }
        
        # Create temporary file with test data
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(self.test_responses, self.temp_file)
        self.temp_file.close()
        
        self.engine = ResponseEngine(self.temp_file.name)
    
    def tearDown(self):
        """Clean up test fixtures."""
        Path(self.temp_file.name).unlink()
    
    def test_initialization_with_valid_file(self):
        """Test that engine initializes correctly with valid JSON file."""
        self.assertIsInstance(self.engine, ResponseEngine)
        self.assertIn('test_category', self.engine.categories)
        self.assertIn('fallback', self.engine.categories)
    
    def test_initialization_with_invalid_file(self):
        """Test that engine falls back gracefully with invalid file."""
        engine = ResponseEngine('nonexistent_file.json')
        self.assertIsInstance(engine, ResponseEngine)
        self.assertIn('fallback', engine.categories)
    
    def test_load_responses_structure(self):
        """Test that responses are loaded with correct structure."""
        category = self.engine.categories['test_category']
        self.assertIsInstance(category, ResponseCategory)
        self.assertEqual(category.name, 'test_category')
        self.assertEqual(category.keywords, ['test', 'sample'])
        self.assertEqual(len(category.responses), 2)
        self.assertEqual(len(category.furby_sounds), 3)
        self.assertEqual(len(category.furbish_phrases), 2)
        
        # Check furbish phrases are tuples
        for phrase in category.furbish_phrases:
            self.assertIsInstance(phrase, tuple)
            self.assertEqual(len(phrase), 2)
    
    def test_get_response_valid_category(self):
        """Test getting response for valid category."""
        response = self.engine.get_response('test_category')
        
        self.assertIsInstance(response, FurbyResponse)
        self.assertIsNotNone(response.base_message)
        self.assertIsNotNone(response.formatted_output)
        self.assertIn(response.base_message, self.test_responses['categories']['test_category']['responses'])
    
    def test_get_response_invalid_category(self):
        """Test getting response for invalid category falls back correctly."""
        response = self.engine.get_response('nonexistent_category')
        
        self.assertIsInstance(response, FurbyResponse)
        self.assertIsNotNone(response.base_message)
        # Should fall back to fallback category
        self.assertIn(response.base_message, self.test_responses['categories']['fallback']['responses'])
    
    def test_get_response_with_emotion(self):
        """Test getting response with emotion parameter."""
        response = self.engine.get_response('test_category', 'happy')
        
        self.assertIsInstance(response, FurbyResponse)
        self.assertIsNotNone(response.formatted_output)
    
    def test_add_furby_flair(self):
        """Test that Furby flair is added appropriately."""
        category = self.engine.categories['test_category']
        original_message = "Test message"
        
        # Test multiple times to account for randomness
        results = []
        for _ in range(10):
            enhanced = self.engine.add_furby_flair(original_message, category)
            results.append(enhanced)
        
        # Should always return a string
        for result in results:
            self.assertIsInstance(result, str)
            self.assertGreaterEqual(len(result), len(original_message))
    
    @patch('random.random')
    def test_maybe_add_furbish_with_chance(self, mock_random):
        """Test Furbish phrase addition with controlled randomness."""
        category = self.engine.categories['test_category']
        
        # Test when random returns value < 0.3 (should add Furbish)
        mock_random.return_value = 0.2
        result = self.engine.maybe_add_furbish(category)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        
        # Test when random returns value >= 0.3 (should not add Furbish)
        mock_random.return_value = 0.5
        result = self.engine.maybe_add_furbish(category)
        self.assertIsNone(result)
    
    def test_format_therapeutic_response_basic(self):
        """Test basic response formatting without Furbish."""
        message = "Test therapeutic message"
        formatted = self.engine.format_therapeutic_response(message)
        
        self.assertEqual(formatted, message)
    
    def test_format_therapeutic_response_with_furbish(self):
        """Test response formatting with Furbish phrase."""
        message = "Test therapeutic message"
        furbish_phrase = ("Dah test", "test phrase")
        
        formatted = self.engine.format_therapeutic_response(message, furbish_phrase)
        
        self.assertIn(message, formatted)
        self.assertIn("Dah test!", formatted)
        self.assertIn("(test phrase)", formatted)
    
    def test_get_available_categories(self):
        """Test getting list of available categories."""
        categories = self.engine.get_available_categories()
        
        self.assertIsInstance(categories, list)
        self.assertIn('test_category', categories)
        self.assertIn('fallback', categories)
    
    def test_get_category_info_valid(self):
        """Test getting info for valid category."""
        info = self.engine.get_category_info('test_category')
        
        self.assertIsInstance(info, ResponseCategory)
        self.assertEqual(info.name, 'test_category')
    
    def test_get_category_info_invalid(self):
        """Test getting info for invalid category."""
        info = self.engine.get_category_info('nonexistent')
        
        self.assertIsNone(info)
    
    def test_response_consistency(self):
        """Test that responses are consistent and well-formed."""
        # Test multiple responses from same category
        responses = []
        for _ in range(5):
            response = self.engine.get_response('test_category')
            responses.append(response)
        
        for response in responses:
            # All responses should be FurbyResponse objects
            self.assertIsInstance(response, FurbyResponse)
            
            # Should have required fields
            self.assertIsNotNone(response.base_message)
            self.assertIsNotNone(response.formatted_output)
            self.assertIsNotNone(response.furby_sounds)
            
            # Formatted output should contain base message
            self.assertIn(response.base_message.split('*')[0].strip(), 
                         response.formatted_output.split('*')[0].strip())
    
    def test_therapeutic_framing_maintained(self):
        """Test that therapeutic framing is maintained in responses."""
        response = self.engine.get_response('test_category')
        
        # Response should be supportive and positive
        formatted_lower = response.formatted_output.lower()
        
        # Should not contain negative or harmful language
        harmful_words = ['stupid', 'wrong', 'bad', 'failure', 'worthless']
        for word in harmful_words:
            self.assertNotIn(word, formatted_lower)
    
    def test_furby_personality_elements(self):
        """Test that Furby personality elements are present."""
        response = self.engine.get_response('test_category')
        
        # Should contain Furby-style elements
        furby_indicators = ['*', 'me ', 'furby', 'ooh', 'eee', 'chirp', 'purr']
        has_furby_element = any(indicator in response.formatted_output.lower() 
                               for indicator in furby_indicators)
        
        self.assertTrue(has_furby_element, 
                       f"Response should contain Furby personality elements: {response.formatted_output}")
    
    def test_response_caching(self):
        """Test that responses are cached for repeat functionality."""
        # Initially no cached response
        self.assertFalse(self.engine.has_cached_response())
        
        # Generate a response
        response = self.engine.get_response('test_category')
        
        # Should now have cached response
        self.assertTrue(self.engine.has_cached_response())
        self.assertIsNotNone(response.clean_version)
    
    def test_clean_version_creation(self):
        """Test that clean versions are created properly."""
        response = self.engine.get_response('test_category')
        
        # Should have a clean version
        self.assertIsNotNone(response.clean_version)
        self.assertIsInstance(response.clean_version, str)
        self.assertGreater(len(response.clean_version), 0)
        
        # Clean version should be different from formatted output (usually)
        # Note: might be same if no Furbish was added, so we check content
        self.assertTrue(len(response.clean_version) > 0)
    
    def test_create_clean_version_removes_sounds(self):
        """Test that _create_clean_version removes excessive Furby sounds."""
        test_message = "Hello! *chirp* *purr* How are you? *giggle* ooh! eee!"
        clean = self.engine._create_clean_version(test_message)
        
        # Should remove most sound effects
        self.assertNotIn('*chirp*', clean)
        self.assertNotIn('*purr*', clean)
        self.assertNotIn('*giggle*', clean)
        self.assertNotIn('ooh!', clean)
        self.assertNotIn('eee!', clean)
        
        # Should preserve the main message
        self.assertIn('Hello', clean)
        self.assertIn('How are you', clean)
    
    def test_create_clean_version_handles_multiple_sounds(self):
        """Test that consecutive sound effects are handled properly."""
        test_message = "Test *chirp* *purr* message"
        clean = self.engine._create_clean_version(test_message)
        
        # Should handle consecutive sounds
        self.assertIn('Test', clean)
        self.assertIn('message', clean)
        # Should not have the original consecutive sounds
        self.assertNotIn('*chirp* *purr*', clean)
    
    def test_get_repeat_response_with_cache(self):
        """Test getting repeat response when cache exists."""
        # Generate initial response
        original = self.engine.get_response('test_category')
        
        # Get repeat response
        repeat = self.engine.get_repeat_response()
        
        self.assertIsNotNone(repeat)
        self.assertIsInstance(repeat, FurbyResponse)
        
        # Repeat should use clean version
        self.assertEqual(repeat.formatted_output, original.clean_version)
        
        # Repeat should not have Furbish phrase
        self.assertIsNone(repeat.furbish_phrase)
        
        # Should have same base message
        self.assertEqual(repeat.base_message, original.base_message)
    
    def test_get_repeat_response_without_cache(self):
        """Test getting repeat response when no cache exists."""
        # Clear any existing cache
        self.engine.clear_cache()
        
        # Try to get repeat response
        repeat = self.engine.get_repeat_response()
        
        self.assertIsNone(repeat)
    
    def test_cache_management(self):
        """Test cache management methods."""
        # Initially no cache
        self.assertFalse(self.engine.has_cached_response())
        
        # Generate response creates cache
        self.engine.get_response('test_category')
        self.assertTrue(self.engine.has_cached_response())
        
        # Clear cache removes it
        self.engine.clear_cache()
        self.assertFalse(self.engine.has_cached_response())
    
    def test_repeat_response_maintains_therapeutic_content(self):
        """Test that repeat responses maintain therapeutic value."""
        # Generate response with therapeutic content
        original = self.engine.get_response('test_category')
        repeat = self.engine.get_repeat_response()
        
        self.assertIsNotNone(repeat)
        
        # Should maintain core therapeutic message
        # The clean version should still be supportive
        self.assertGreater(len(repeat.formatted_output), 5)
        
        # Should not contain harmful language
        harmful_words = ['stupid', 'wrong', 'bad', 'failure']
        for word in harmful_words:
            self.assertNotIn(word, repeat.formatted_output.lower())
    
    def test_clean_version_proper_formatting(self):
        """Test that clean versions have proper formatting."""
        test_cases = [
            "Hello *chirp* world",
            "Test message *purr* *giggle* end",
            "Simple message",
            "Message with ooh! and eee! sounds",
            ""
        ]
        
        for test_message in test_cases:
            with self.subTest(message=test_message):
                clean = self.engine._create_clean_version(test_message)
                
                if test_message.strip():
                    # Should end with proper punctuation
                    self.assertTrue(clean.endswith(('.', '!', '?')) or not clean)
                    
                    # Should not have excessive whitespace
                    self.assertEqual(clean, clean.strip())
                    self.assertNotIn('  ', clean)  # No double spaces


class TestResponseEngineIntegration(unittest.TestCase):
    """Integration tests using the actual responses.json file."""
    
    def setUp(self):
        """Set up with real responses file."""
        # Use the actual responses.json file
        responses_file = Path(__file__).parent.parent / "furby_therapist" / "responses.json"
        if responses_file.exists():
            self.engine = ResponseEngine(str(responses_file))
        else:
            self.skipTest("responses.json file not found")
    
    def test_all_categories_work(self):
        """Test that all categories in the real file work correctly."""
        categories = self.engine.get_available_categories()
        
        for category in categories:
            with self.subTest(category=category):
                response = self.engine.get_response(category)
                self.assertIsInstance(response, FurbyResponse)
                self.assertIsNotNone(response.formatted_output)
                self.assertTrue(len(response.formatted_output) > 0)
    
    def test_real_therapeutic_quality(self):
        """Test therapeutic quality with real responses."""
        test_categories = ['sadness', 'anxiety', 'anger', 'happiness', 'loneliness']
        
        for category in test_categories:
            if category in self.engine.get_available_categories():
                with self.subTest(category=category):
                    response = self.engine.get_response(category)
                    
                    # Should be supportive and empathetic
                    self.assertGreater(len(response.formatted_output), 10)
                    
                    # Should contain Furby elements
                    self.assertTrue('*' in response.formatted_output or 
                                  'me ' in response.formatted_output.lower())


if __name__ == '__main__':
    unittest.main()