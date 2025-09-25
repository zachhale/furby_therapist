"""
Unit tests for the FurbyTherapist library interface.
"""

import unittest
from unittest.mock import patch, MagicMock, mock_open
import tempfile
import json
from pathlib import Path

from furby_therapist import FurbyTherapist, create_furby_therapist, process_single_query
from furby_therapist.models import FurbyResponse


class TestFurbyTherapistLibrary(unittest.TestCase):
    """Test the FurbyTherapist library class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a minimal responses.json for testing
        self.test_responses = {
            "categories": {
                "sadness": {
                    "keywords": ["sad", "down", "depressed"],
                    "responses": ["*gentle purr* Furby understands sadness! You're not alone! *supportive chirp*"],
                    "furby_sounds": ["*gentle purr*", "*supportive chirp*"],
                    "furbish_phrases": [["Dah koh-koh", "it's okay"]]
                },
                "happiness": {
                    "keywords": ["happy", "joy", "glad"],
                    "responses": ["*excited chirp* Yay! Furby loves happy feelings! *joyful beep*"],
                    "furby_sounds": ["*excited chirp*", "*joyful beep*"],
                    "furbish_phrases": [["Noo-loo", "happy"]]
                },
                "fallback": {
                    "keywords": [],
                    "responses": ["*gentle chirp* Furby is here to listen! Tell me more! *encouraging beep*"],
                    "furby_sounds": ["*gentle chirp*", "*encouraging beep*"],
                    "furbish_phrases": [["U-nye way-loh", "you matter"]]
                }
            }
        }
        
        # Create temporary file
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(self.test_responses, self.temp_file)
        self.temp_file.close()
    
    def tearDown(self):
        """Clean up test fixtures."""
        Path(self.temp_file.name).unlink(missing_ok=True)
    
    @patch('furby_therapist.core.responses.open', new_callable=mock_open)
    @patch('furby_therapist.core.responses.Path')
    @patch('furby_therapist.core.database.ResponseDatabase')
    def test_library_initialization_standard_mode(self, mock_db, mock_path, mock_file):
        """Test library initialization in standard mode."""
        mock_file.return_value.read.return_value = json.dumps(self.test_responses)
        mock_path.return_value.__truediv__.return_value = self.temp_file.name
        
        # Mock the database to return test categories
        mock_db_instance = MagicMock()
        mock_db_instance.get_all_categories.return_value = {}
        mock_db.return_value = mock_db_instance
        
        therapist = FurbyTherapist(cycling_mode=False, maintain_session=True)
        
        self.assertFalse(therapist.is_cycling_mode())
        self.assertTrue(therapist.is_stateful())
        self.assertIsNotNone(therapist.get_conversation_history())
    
    @patch('furby_therapist.core.responses.open', new_callable=mock_open)
    @patch('furby_therapist.core.responses.Path')
    @patch('furby_therapist.core.database.ResponseDatabase')
    def test_library_initialization_cycling_mode(self, mock_db, mock_path, mock_file):
        """Test library initialization in cycling mode."""
        mock_file.return_value.read.return_value = json.dumps(self.test_responses)
        mock_path.return_value.__truediv__.return_value = self.temp_file.name
        
        # Mock the database to return test categories
        mock_db_instance = MagicMock()
        mock_db_instance.get_all_categories.return_value = {}
        mock_db.return_value = mock_db_instance
        
        therapist = FurbyTherapist(cycling_mode=True, maintain_session=False)
        
        self.assertTrue(therapist.is_cycling_mode())
        self.assertFalse(therapist.is_stateful())
        self.assertIsNone(therapist.get_conversation_history())
    
    @patch('furby_therapist.core.responses.open', new_callable=mock_open)
    @patch('furby_therapist.core.responses.Path')
    @patch('furby_therapist.core.database.ResponseDatabase')
    def test_process_query_valid_input(self, mock_db, mock_path, mock_file):
        """Test processing a valid query."""
        mock_file.return_value.read.return_value = json.dumps(self.test_responses)
        mock_path.return_value.__truediv__.return_value = self.temp_file.name
        
        # Mock the database to return test categories
        mock_db_instance = MagicMock()
        mock_db_instance.get_all_categories.return_value = {}
        mock_db.return_value = mock_db_instance
        
        therapist = FurbyTherapist(cycling_mode=False, maintain_session=True)
        response = therapist.process_query("I'm feeling sad today")
        
        self.assertIsInstance(response, FurbyResponse)
        self.assertIsNotNone(response.base_message)
        self.assertIsNotNone(response.formatted_output)
    
    @patch('furby_therapist.core.responses.open', new_callable=mock_open)
    @patch('furby_therapist.core.responses.Path')
    @patch('furby_therapist.core.database.ResponseDatabase')
    def test_process_query_empty_input(self, mock_db, mock_path, mock_file):
        """Test processing empty input."""
        mock_file.return_value.read.return_value = json.dumps(self.test_responses)
        mock_path.return_value.__truediv__.return_value = self.temp_file.name
        
        # Mock the database to return test categories
        mock_db_instance = MagicMock()
        mock_db_instance.get_all_categories.return_value = {}
        mock_db.return_value = mock_db_instance
        
        therapist = FurbyTherapist(cycling_mode=False, maintain_session=True)
        response = therapist.process_query("")
        
        self.assertIsInstance(response, FurbyResponse)
        self.assertIn("listening", response.formatted_output.lower())
    
    @patch('furby_therapist.core.responses.open', new_callable=mock_open)
    @patch('furby_therapist.core.responses.Path')
    @patch('furby_therapist.core.database.ResponseDatabase')
    def test_process_query_invalid_input(self, mock_db, mock_path, mock_file):
        """Test processing invalid input."""
        mock_file.return_value.read.return_value = json.dumps(self.test_responses)
        mock_path.return_value.__truediv__.return_value = self.temp_file.name
        
        # Mock the database to return test categories
        mock_db_instance = MagicMock()
        mock_db_instance.get_all_categories.return_value = {}
        mock_db.return_value = mock_db_instance
        
        therapist = FurbyTherapist(cycling_mode=False, maintain_session=True)
        
        # Test extremely long input
        long_input = "x" * 2000
        with self.assertRaises(ValueError):
            therapist.process_query(long_input)
    
    @patch('furby_therapist.core.responses.open', new_callable=mock_open)
    @patch('furby_therapist.core.responses.Path')
    @patch('furby_therapist.core.database.ResponseDatabase')
    def test_get_available_categories(self, mock_db, mock_path, mock_file):
        """Test getting available categories."""
        mock_file.return_value.read.return_value = json.dumps(self.test_responses)
        mock_path.return_value.__truediv__.return_value = self.temp_file.name
        
        # Mock the database to return test categories
        mock_db_instance = MagicMock()
        mock_db_instance.get_all_categories.return_value = {}
        mock_db.return_value = mock_db_instance
        
        therapist = FurbyTherapist(cycling_mode=False, maintain_session=True)
        categories = therapist.get_available_categories()
        
        self.assertIsInstance(categories, list)
    
    @patch('furby_therapist.core.responses.open', new_callable=mock_open)
    @patch('furby_therapist.core.responses.Path')
    @patch('furby_therapist.core.database.ResponseDatabase')
    def test_get_category_info(self, mock_db, mock_path, mock_file):
        """Test getting category information."""
        mock_file.return_value.read.return_value = json.dumps(self.test_responses)
        mock_path.return_value.__truediv__.return_value = self.temp_file.name
        
        # Mock the database to return test categories
        mock_db_instance = MagicMock()
        mock_db_instance.get_all_categories.return_value = {}
        mock_db.return_value = mock_db_instance
        
        therapist = FurbyTherapist(cycling_mode=False, maintain_session=True)
        category_info = therapist.get_category_info("sadness")
        
        # This will return None since we're mocking, which is fine for the test
        # The important thing is that the method doesn't crash
    
    @patch('furby_therapist.core.responses.open', new_callable=mock_open)
    @patch('furby_therapist.core.responses.Path')
    @patch('furby_therapist.core.database.ResponseDatabase')
    def test_conversation_history_stateful(self, mock_db, mock_path, mock_file):
        """Test conversation history in stateful mode."""
        mock_file.return_value.read.return_value = json.dumps(self.test_responses)
        mock_path.return_value.__truediv__.return_value = self.temp_file.name
        
        # Mock the database to return test categories
        mock_db_instance = MagicMock()
        mock_db_instance.get_all_categories.return_value = {}
        mock_db.return_value = mock_db_instance
        
        therapist = FurbyTherapist(cycling_mode=False, maintain_session=True)
        
        # Process a query to add to history
        therapist.process_query("I'm feeling happy")
        
        # Check session stats
        stats = therapist.get_session_stats()
        self.assertTrue(stats["stateful_mode"])
        self.assertEqual(stats["conversation_length"], 1)
        self.assertFalse(stats["cycling_mode"])
    
    @patch('furby_therapist.core.responses.open', new_callable=mock_open)
    @patch('furby_therapist.core.responses.Path')
    @patch('furby_therapist.core.database.ResponseDatabase')
    def test_conversation_history_stateless(self, mock_db, mock_path, mock_file):
        """Test conversation history in stateless mode."""
        mock_file.return_value.read.return_value = json.dumps(self.test_responses)
        mock_path.return_value.__truediv__.return_value = self.temp_file.name
        
        # Mock the database to return test categories
        mock_db_instance = MagicMock()
        mock_db_instance.get_all_categories.return_value = {}
        mock_db.return_value = mock_db_instance
        
        therapist = FurbyTherapist(cycling_mode=False, maintain_session=False)
        
        # Process a query
        therapist.process_query("I'm feeling happy")
        
        # Check session stats
        stats = therapist.get_session_stats()
        self.assertFalse(stats["stateful_mode"])
    
    @patch('furby_therapist.core.responses.open', new_callable=mock_open)
    @patch('furby_therapist.core.responses.Path')
    @patch('furby_therapist.core.database.ResponseDatabase')
    def test_clear_conversation_history(self, mock_db, mock_path, mock_file):
        """Test clearing conversation history."""
        mock_file.return_value.read.return_value = json.dumps(self.test_responses)
        mock_path.return_value.__truediv__.return_value = self.temp_file.name
        
        # Mock the database to return test categories
        mock_db_instance = MagicMock()
        mock_db_instance.get_all_categories.return_value = {}
        mock_db.return_value = mock_db_instance
        
        therapist = FurbyTherapist(cycling_mode=False, maintain_session=True)
        
        # Add some conversation history
        therapist.process_query("I'm feeling sad")
        stats_before = therapist.get_session_stats()
        self.assertEqual(stats_before["conversation_length"], 1)
        
        # Clear history
        therapist.clear_conversation_history()
        stats_after = therapist.get_session_stats()
        self.assertEqual(stats_after["conversation_length"], 0)
    
    @patch('furby_therapist.core.responses.open', new_callable=mock_open)
    @patch('furby_therapist.core.responses.Path')
    @patch('furby_therapist.core.database.ResponseDatabase')
    def test_greetings(self, mock_db, mock_path, mock_file):
        """Test morning and night greetings."""
        mock_file.return_value.read.return_value = json.dumps(self.test_responses)
        mock_path.return_value.__truediv__.return_value = self.temp_file.name
        
        # Mock the database to return test categories
        mock_db_instance = MagicMock()
        mock_db_instance.get_all_categories.return_value = {}
        mock_db.return_value = mock_db_instance
        
        therapist = FurbyTherapist(cycling_mode=False, maintain_session=True)
        
        morning_greeting = therapist.get_good_morning_greeting()
        self.assertIsInstance(morning_greeting, str)
        self.assertIn("morning", morning_greeting.lower())
        
        night_greeting = therapist.get_good_night_greeting()
        self.assertIsInstance(night_greeting, str)
        # Check for night-related words like "dreams", "sleep", or "tomorrow"
        night_words = ["dreams", "sleep", "tomorrow", "night"]
        has_night_word = any(word in night_greeting.lower() for word in night_words)
        self.assertTrue(has_night_word, f"Night greeting should contain night-related words: {night_greeting}")
    
    @patch('furby_therapist.core.responses.open', new_callable=mock_open)
    @patch('furby_therapist.core.responses.Path')
    @patch('furby_therapist.core.database.ResponseDatabase')
    def test_repeat_functionality(self, mock_db, mock_path, mock_file):
        """Test repeat functionality."""
        mock_file.return_value.read.return_value = json.dumps(self.test_responses)
        mock_path.return_value.__truediv__.return_value = self.temp_file.name
        
        # Mock the database to return test categories
        mock_db_instance = MagicMock()
        mock_db_instance.get_all_categories.return_value = {}
        mock_db.return_value = mock_db_instance
        
        therapist = FurbyTherapist(cycling_mode=False, maintain_session=True)
        
        # Initially no cached response
        self.assertFalse(therapist.has_cached_response())
        self.assertIsNone(therapist.get_repeat_response())
        
        # Process a query to cache a response
        therapist.process_query("I'm feeling happy")
        
        # Now should have cached response
        self.assertTrue(therapist.has_cached_response())
        repeat_response = therapist.get_repeat_response()
        self.assertIsNotNone(repeat_response)
        self.assertIsInstance(repeat_response, FurbyResponse)
        
        # Clear cache
        therapist.clear_response_cache()
        self.assertFalse(therapist.has_cached_response())
    
    @patch('furby_therapist.core.responses.open', new_callable=mock_open)
    @patch('furby_therapist.core.responses.Path')
    @patch('furby_therapist.core.database.ResponseDatabase')
    def test_cleanup(self, mock_db, mock_path, mock_file):
        """Test cleanup functionality."""
        mock_file.return_value.read.return_value = json.dumps(self.test_responses)
        mock_path.return_value.__truediv__.return_value = self.temp_file.name
        
        # Mock the database to return test categories
        mock_db_instance = MagicMock()
        mock_db_instance.get_all_categories.return_value = {}
        mock_db.return_value = mock_db_instance
        
        therapist = FurbyTherapist(cycling_mode=False, maintain_session=True)
        
        # Should not raise any exceptions
        therapist.cleanup()


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a minimal responses.json for testing
        self.test_responses = {
            "categories": {
                "fallback": {
                    "keywords": [],
                    "responses": ["*gentle chirp* Furby is here to listen!"],
                    "furby_sounds": ["*gentle chirp*"],
                    "furbish_phrases": [["U-nye way-loh", "you matter"]]
                }
            }
        }
        
        # Create temporary file
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(self.test_responses, self.temp_file)
        self.temp_file.close()
    
    def tearDown(self):
        """Clean up test fixtures."""
        Path(self.temp_file.name).unlink(missing_ok=True)
    
    @patch('furby_therapist.core.responses.open', new_callable=mock_open)
    @patch('furby_therapist.core.responses.Path')
    @patch('furby_therapist.core.database.ResponseDatabase')
    def test_create_furby_therapist(self, mock_db, mock_path, mock_file):
        """Test the create_furby_therapist convenience function."""
        mock_file.return_value.read.return_value = json.dumps(self.test_responses)
        mock_path.return_value.__truediv__.return_value = self.temp_file.name
        
        # Mock the database to return test categories
        mock_db_instance = MagicMock()
        mock_db_instance.get_all_categories.return_value = {}
        mock_db.return_value = mock_db_instance
        
        # Test default parameters
        therapist = create_furby_therapist()
        self.assertFalse(therapist.is_cycling_mode())
        self.assertTrue(therapist.is_stateful())
        
        # Test with parameters
        therapist = create_furby_therapist(cycling_mode=True, stateful=False)
        self.assertTrue(therapist.is_cycling_mode())
        self.assertFalse(therapist.is_stateful())
    
    @patch('furby_therapist.core.responses.open', new_callable=mock_open)
    @patch('furby_therapist.core.responses.Path')
    @patch('furby_therapist.core.database.ResponseDatabase')
    def test_process_single_query_function(self, mock_db, mock_path, mock_file):
        """Test the process_single_query convenience function."""
        mock_file.return_value.read.return_value = json.dumps(self.test_responses)
        mock_path.return_value.__truediv__.return_value = self.temp_file.name
        
        # Mock the database to return test categories
        mock_db_instance = MagicMock()
        mock_db_instance.get_all_categories.return_value = {}
        mock_db.return_value = mock_db_instance
        
        response = process_single_query("Hello Furby", cycling_mode=False)
        
        self.assertIsInstance(response, FurbyResponse)
        self.assertIsNotNone(response.formatted_output)
    
    @patch('furby_therapist.core.responses.open', new_callable=mock_open)
    @patch('furby_therapist.core.responses.Path')
    @patch('furby_therapist.core.database.ResponseDatabase')
    def test_process_single_query_function_invalid_input(self, mock_db, mock_path, mock_file):
        """Test the process_single_query convenience function with invalid input."""
        mock_file.return_value.read.return_value = json.dumps(self.test_responses)
        mock_path.return_value.__truediv__.return_value = self.temp_file.name
        
        # Mock the database to return test categories
        mock_db_instance = MagicMock()
        mock_db_instance.get_all_categories.return_value = {}
        mock_db.return_value = mock_db_instance
        
        # Test with invalid input
        with self.assertRaises(ValueError):
            process_single_query("x" * 2000, cycling_mode=False)


class TestLibraryErrorHandling(unittest.TestCase):
    """Test error handling in the library."""
    
    def test_initialization_failure(self):
        """Test library initialization failure."""
        # Try to initialize with non-existent response file
        with patch('furby_therapist.core.library.ResponseDatabase') as mock_db:
            mock_db.side_effect = Exception("Database initialization failed")
            
            with self.assertRaises(RuntimeError):
                FurbyTherapist(cycling_mode=False, maintain_session=True)
    
    @patch('furby_therapist.core.responses.open', new_callable=mock_open)
    @patch('furby_therapist.core.responses.Path')
    @patch('furby_therapist.core.database.ResponseDatabase')
    def test_processing_failure_recovery(self, mock_db, mock_path, mock_file):
        """Test recovery from processing failures."""
        # Create minimal test data
        test_responses = {
            "categories": {
                "fallback": {
                    "keywords": [],
                    "responses": ["Fallback response"],
                    "furby_sounds": ["*chirp*"],
                    "furbish_phrases": []
                }
            }
        }
        
        mock_file.return_value.read.return_value = json.dumps(test_responses)
        mock_path.return_value.__truediv__.return_value = "test.json"
        
        # Mock the database to return test categories
        mock_db_instance = MagicMock()
        mock_db_instance.get_all_categories.return_value = {}
        mock_db.return_value = mock_db_instance
        
        therapist = FurbyTherapist(cycling_mode=False, maintain_session=True)
        
        # Mock a processing failure in the processor
        with patch.object(therapist.processor, 'process_query') as mock_process:
            mock_process.side_effect = Exception("Processing failed")
            
            with self.assertRaises(RuntimeError):
                therapist.process_query("test query")


if __name__ == '__main__':
    unittest.main()