"""
Unit tests for the Furby response engine.
"""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from furby_therapist.core.responses import ResponseEngine
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
        # Find the project root by looking for furby_therapist directory
        current_path = Path(__file__).resolve()
        project_root = None
        
        # Walk up the directory tree to find the project root
        for parent in current_path.parents:
            if (parent / "furby_therapist").exists():
                project_root = parent
                break
        
        if project_root is None:
            self.skipTest("Could not find project root directory")
        
        responses_file = project_root / "furby_therapist" / "data" / "responses.json"
        if responses_file.exists():
            self.engine = ResponseEngine(str(responses_file))
        else:
            self.skipTest(f"responses.json file not found at {responses_file}")
    
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
    
    def test_bicycle_category_responses(self):
        """Test bicycle category responses if available."""
        if 'bicycle' in self.engine.get_available_categories():
            response = self.engine.get_response('bicycle')
            
            # Should be a valid response
            self.assertIsInstance(response, FurbyResponse)
            self.assertGreater(len(response.formatted_output), 10)
            
            # Should contain bicycle-themed content
            bicycle_indicators = ['bike', 'bicycle', 'cycling', 'pedal', 'wheel', 'chain']
            has_bicycle_content = any(indicator in response.formatted_output.lower() 
                                    for indicator in bicycle_indicators)
            self.assertTrue(has_bicycle_content, 
                          f"Bicycle response should contain bicycle-themed content: {response.formatted_output}")
            
            # Should maintain therapeutic value
            therapeutic_indicators = ['balance', 'forward', 'journey', 'progress', 'support', 'care']
            has_therapeutic_content = any(indicator in response.formatted_output.lower() 
                                        for indicator in therapeutic_indicators)
            self.assertTrue(has_therapeutic_content or len(response.formatted_output) > 20,
                          f"Bicycle response should maintain therapeutic value: {response.formatted_output}")
            
            # Should contain Furby elements
            furby_indicators = ['*', 'me ', 'furby', 'wee-tah', 'ooh', 'eee']
            has_furby_element = any(indicator in response.formatted_output.lower() 
                                  for indicator in furby_indicators)
            self.assertTrue(has_furby_element,
                          f"Bicycle response should contain Furby personality: {response.formatted_output}")


class TestBicycleResponseEngine(unittest.TestCase):
    """Test cases specifically for bicycle-themed responses."""
    
    def setUp(self):
        """Set up test fixtures with bicycle responses."""
        # Create test responses including bicycle category
        self.test_responses = {
            "schema_version": "1.0",
            "categories": {
                "bicycle": {
                    "keywords": ["bike", "bicycle", "cycling", "riding", "pedal", "chain", "wheel", "maintenance"],
                    "responses": [
                        "Wee-tah! Me love bike-talk! *excited wheel spin sound* Life is like riding bicycle - you keep balance by moving forward! *encouraging chirp*",
                        "Ooh-lah! Cycling makes Furby think of life journey! *gentle pedal sound* Sometimes uphill is hard, but downhill joy comes after! *supportive trill*"
                    ],
                    "furby_sounds": ["*wheel spin*", "*pedal sound*", "*chain click*", "*spoke ping*", "*bell ring*", "wee-tah!", "ooh-lah!"],
                    "furbish_phrases": [
                        ["Dah wheel-loh", "keep rolling forward"],
                        ["Kah pedal-may", "pedal with love"],
                        ["U-nye cycle-way", "you are strong rider"]
                    ]
                },
                "fallback": {
                    "keywords": [],
                    "responses": ["Fallback response! *gentle chirp*"],
                    "furby_sounds": ["*chirp*"],
                    "furbish_phrases": [["Dah koh-koh", "it's okay"]]
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
    
    def test_bicycle_category_loaded(self):
        """Test that bicycle category is loaded correctly."""
        self.assertIn('bicycle', self.engine.categories)
        
        bicycle_category = self.engine.categories['bicycle']
        self.assertEqual(bicycle_category.name, 'bicycle')
        self.assertIn('bike', bicycle_category.keywords)
        self.assertIn('cycling', bicycle_category.keywords)
        self.assertGreater(len(bicycle_category.responses), 0)
        self.assertGreater(len(bicycle_category.furby_sounds), 0)
        self.assertGreater(len(bicycle_category.furbish_phrases), 0)
    
    def test_bicycle_response_generation(self):
        """Test generating bicycle-themed responses."""
        response = self.engine.get_response('bicycle')
        
        self.assertIsInstance(response, FurbyResponse)
        self.assertIsNotNone(response.formatted_output)
        
        # Should contain bicycle-themed content
        self.assertTrue(any(word in response.formatted_output.lower() 
                          for word in ['bike', 'bicycle', 'cycling', 'wheel', 'pedal']))
    
    def test_bicycle_therapeutic_metaphors(self):
        """Test that bicycle responses contain therapeutic metaphors."""
        # Generate multiple responses to test different metaphors
        responses = []
        for _ in range(10):
            response = self.engine.get_response('bicycle')
            responses.append(response.formatted_output.lower())
        
        # Check for therapeutic bicycle metaphors
        therapeutic_concepts = ['balance', 'forward', 'journey', 'uphill', 'downhill', 'progress']
        
        has_therapeutic_metaphor = any(
            any(concept in response for concept in therapeutic_concepts)
            for response in responses
        )
        
        self.assertTrue(has_therapeutic_metaphor, 
                       "Bicycle responses should contain therapeutic metaphors")
    
    def test_bicycle_furby_sounds(self):
        """Test that bicycle responses use appropriate Furby sounds."""
        response = self.engine.get_response('bicycle')
        
        # Should contain bicycle-themed Furby sounds
        bicycle_sounds = ['wheel spin', 'pedal sound', 'chain click', 'spoke ping', 'bell ring']
        
        has_bicycle_sound = any(sound.replace(' ', '') in response.formatted_output.replace(' ', '').lower() 
                               for sound in bicycle_sounds)
        
        # Should have some kind of sound effect
        has_sound_effect = '*' in response.formatted_output
        
        self.assertTrue(has_sound_effect, "Bicycle response should contain sound effects")
    
    def test_bicycle_furbish_phrases(self):
        """Test bicycle-specific Furbish phrases."""
        bicycle_category = self.engine.categories['bicycle']
        
        # Check that bicycle-specific Furbish phrases exist
        furbish_phrases = bicycle_category.furbish_phrases
        self.assertGreater(len(furbish_phrases), 0)
        
        # Check that they're cycling-themed
        cycling_themed_phrases = ['wheel-loh', 'pedal-may', 'cycle-way']
        
        has_cycling_furbish = any(
            any(theme in phrase[0] for theme in cycling_themed_phrases)
            for phrase in furbish_phrases
        )
        
        self.assertTrue(has_cycling_furbish, 
                       "Should have cycling-themed Furbish phrases")
    
    def test_bicycle_response_variety(self):
        """Test that bicycle responses have good variety."""
        responses = []
        for _ in range(20):
            response = self.engine.get_response('bicycle')
            responses.append(response.formatted_output)
        
        # Should have some variety in responses
        unique_responses = set(responses)
        self.assertGreater(len(unique_responses), 1, 
                          "Should have variety in bicycle responses")
    
    def test_bicycle_maintains_therapeutic_value(self):
        """Test that bicycle easter eggs maintain therapeutic value."""
        response = self.engine.get_response('bicycle')
        
        # Should not contain harmful or negative language
        harmful_words = ['stupid', 'wrong', 'bad', 'failure', 'worthless', 'hate']
        for word in harmful_words:
            self.assertNotIn(word, response.formatted_output.lower())
        
        # Should be supportive and positive
        self.assertGreater(len(response.formatted_output), 20)
        
        # Should maintain Furby personality
        self.assertTrue('*' in response.formatted_output or 
                       'me ' in response.formatted_output.lower() or
                       any(exclamation in response.formatted_output 
                           for exclamation in ['wee-tah', 'ooh-lah', 'eee']))
    
    def test_bicycle_clean_version_creation(self):
        """Test that bicycle responses create appropriate clean versions."""
        response = self.engine.get_response('bicycle')
        
        self.assertIsNotNone(response.clean_version)
        self.assertIsInstance(response.clean_version, str)
        self.assertGreater(len(response.clean_version), 0)
        
        # Clean version should maintain therapeutic bicycle content
        self.assertTrue(any(word in response.clean_version.lower() 
                          for word in ['bike', 'bicycle', 'cycling', 'balance', 'forward', 'journey']))
    
    def test_bicycle_repeat_functionality(self):
        """Test repeat functionality with bicycle responses."""
        # Generate initial bicycle response
        original = self.engine.get_response('bicycle')
        
        # Get repeat response
        repeat = self.engine.get_repeat_response()
        
        self.assertIsNotNone(repeat)
        self.assertIsInstance(repeat, FurbyResponse)
        
        # Repeat should maintain bicycle therapeutic content
        self.assertTrue(any(word in repeat.formatted_output.lower() 
                          for word in ['bike', 'bicycle', 'cycling', 'balance', 'forward']))
        
        # Should not have Furbish in repeat
        self.assertIsNone(repeat.furbish_phrase)


if __name__ == '__main__':
    unittest.main()