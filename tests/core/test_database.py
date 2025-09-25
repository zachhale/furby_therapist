"""
Unit tests for the response database module.
"""

import unittest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, mock_open

from furby_therapist.core.database import ResponseDatabase, ResponseCategory


class TestResponseDatabase(unittest.TestCase):
    """Test cases for ResponseDatabase class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create test response data
        self.test_responses = {
            "schema_version": "1.0",
            "categories": {
                "sadness": {
                    "keywords": ["sad", "down", "depressed", "crying"],
                    "responses": [
                        "Test sad response 1 *gentle purr*",
                        "Test sad response 2 *supportive chirp*"
                    ],
                    "furby_sounds": ["*gentle purr*", "*supportive chirp*", "*snuggle*"],
                    "furbish_phrases": [
                        ["Dah koh-koh", "it's okay"],
                        ["Kah may-may", "me love you"]
                    ]
                },
                "happiness": {
                    "keywords": ["happy", "joy", "excited", "glad"],
                    "responses": [
                        "Test happy response 1 *excited chirp*",
                        "Test happy response 2 *joyful trill*"
                    ],
                    "furby_sounds": ["*excited chirp*", "*joyful trill*", "*giggle*"],
                    "furbish_phrases": [
                        ["Wee-tah", "yay"],
                        ["Noo-loo", "happy"]
                    ]
                },
                "fallback": {
                    "keywords": [],
                    "responses": [
                        "Test fallback response *gentle chirp*"
                    ],
                    "furby_sounds": ["*gentle chirp*", "*encouraging beep*"],
                    "furbish_phrases": [
                        ["U-nye way-loh", "you matter"]
                    ]
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
    
    def test_initialization_with_valid_file(self):
        """Test database initializes correctly with valid JSON file."""
        db = ResponseDatabase(self.temp_file.name)
        
        self.assertIsInstance(db, ResponseDatabase)
        categories = db.get_all_categories()
        self.assertIn('sadness', categories)
        self.assertIn('happiness', categories)
        self.assertIn('fallback', categories)
    
    def test_initialization_with_default_file(self):
        """Test database initializes with default responses.json file."""
        # This will use the actual responses.json file if it exists
        try:
            db = ResponseDatabase()
            self.assertIsInstance(db, ResponseDatabase)
            categories = db.get_all_categories()
            self.assertIsInstance(categories, dict)
            self.assertGreater(len(categories), 0)
        except RuntimeError:
            # If responses.json doesn't exist, that's expected in test environment
            self.skipTest("Default responses.json file not found")
    
    def test_get_all_categories_structure(self):
        """Test that get_all_categories returns properly structured data."""
        db = ResponseDatabase(self.temp_file.name)
        categories = db.get_all_categories()
        
        self.assertIsInstance(categories, dict)
        
        for category_name, category in categories.items():
            self.assertIsInstance(category, ResponseCategory)
            self.assertEqual(category.name, category_name)
            self.assertIsInstance(category.keywords, list)
            self.assertIsInstance(category.responses, list)
            self.assertIsInstance(category.furby_sounds, list)
            self.assertIsInstance(category.furbish_phrases, list)
            
            # Check furbish phrases are tuples
            for phrase in category.furbish_phrases:
                self.assertIsInstance(phrase, tuple)
                self.assertEqual(len(phrase), 2)
    
    def test_get_category_valid(self):
        """Test getting a valid category."""
        db = ResponseDatabase(self.temp_file.name)
        
        sadness_category = db.get_category('sadness')
        self.assertIsNotNone(sadness_category)
        self.assertEqual(sadness_category.name, 'sadness')
        self.assertIn('sad', sadness_category.keywords)
        self.assertGreater(len(sadness_category.responses), 0)
    
    def test_get_category_invalid(self):
        """Test getting an invalid category returns None."""
        db = ResponseDatabase(self.temp_file.name)
        
        invalid_category = db.get_category('nonexistent')
        self.assertIsNone(invalid_category)
    
    def test_get_category_names(self):
        """Test getting list of category names."""
        db = ResponseDatabase(self.temp_file.name)
        
        category_names = db.get_category_names()
        self.assertIsInstance(category_names, list)
        self.assertIn('sadness', category_names)
        self.assertIn('happiness', category_names)
        self.assertIn('fallback', category_names)
    
    def test_has_category(self):
        """Test checking if category exists."""
        db = ResponseDatabase(self.temp_file.name)
        
        # Use get_category to check existence
        self.assertIsNotNone(db.get_category('sadness'))
        self.assertIsNotNone(db.get_category('happiness'))
        self.assertIsNone(db.get_category('nonexistent'))
    
    def test_load_responses_with_missing_fields(self):
        """Test that missing required fields cause validation errors."""
        minimal_responses = {
            "schema_version": "1.0",
            "categories": {
                "minimal": {
                    "keywords": ["test"],
                    "responses": ["Test response"]
                    # Missing furby_sounds and furbish_phrases (required fields)
                },
                "fallback": {
                    "keywords": [],
                    "responses": ["Fallback response"],
                    "furby_sounds": ["*chirp*"],
                    "furbish_phrases": []
                }
            }
        }
        
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(minimal_responses, temp_file)
        temp_file.close()
        
        try:
            with self.assertRaises(RuntimeError) as context:
                ResponseDatabase(temp_file.name)
            
            self.assertIn("missing required field", str(context.exception))
        finally:
            Path(temp_file.name).unlink()
    
    def test_load_responses_with_invalid_furbish_format(self):
        """Test that invalid Furbish phrase format causes validation errors."""
        invalid_responses = {
            "schema_version": "1.0",
            "categories": {
                "invalid": {
                    "keywords": ["test"],
                    "responses": ["Test response"],
                    "furby_sounds": ["*chirp*"],
                    "furbish_phrases": [
                        ["valid", "phrase"],
                        ["invalid"]  # Missing translation
                    ]
                },
                "fallback": {
                    "keywords": [],
                    "responses": ["Fallback response"],
                    "furby_sounds": ["*chirp*"],
                    "furbish_phrases": []
                }
            }
        }
        
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(invalid_responses, temp_file)
        temp_file.close()
        
        try:
            with self.assertRaises(RuntimeError) as context:
                ResponseDatabase(temp_file.name)
            
            self.assertIn("furbish phrase", str(context.exception))
        finally:
            Path(temp_file.name).unlink()
    
    def test_schema_version_validation(self):
        """Test that schema version is validated."""
        db = ResponseDatabase(self.temp_file.name)
        
        # Should have loaded the schema version
        self.assertEqual(db.schema_version, "1.0")
    
    def test_category_structure_validation(self):
        """Test that categories have proper structure."""
        db = ResponseDatabase(self.temp_file.name)
        categories = db.get_all_categories()
        
        for category in categories.values():
            self.assertIsInstance(category.name, str)
            self.assertIsInstance(category.keywords, list)
            self.assertIsInstance(category.responses, list)
            self.assertIsInstance(category.furby_sounds, list)
            self.assertIsInstance(category.furbish_phrases, list)
    
    def test_empty_categories_handling(self):
        """Test that empty categories section causes validation error (no fallback)."""
        empty_responses = {
            "schema_version": "1.0",
            "categories": {}
        }
        
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(empty_responses, temp_file)
        temp_file.close()
        
        try:
            with self.assertRaises(RuntimeError) as context:
                ResponseDatabase(temp_file.name)
            
            self.assertIn("fallback", str(context.exception))
        finally:
            Path(temp_file.name).unlink()
    
    def test_duplicate_keywords_handling(self):
        """Test that duplicate keywords are preserved (no deduplication in database)."""
        duplicate_responses = {
            "schema_version": "1.0",
            "categories": {
                "test": {
                    "keywords": ["sad", "sad", "down", "sad"],  # Duplicates
                    "responses": ["Test response"],
                    "furby_sounds": ["*chirp*"],
                    "furbish_phrases": []
                },
                "fallback": {
                    "keywords": [],
                    "responses": ["Fallback response"],
                    "furby_sounds": ["*chirp*"],
                    "furbish_phrases": []
                }
            }
        }
        
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(duplicate_responses, temp_file)
        temp_file.close()
        
        try:
            db = ResponseDatabase(temp_file.name)
            test_category = db.get_category('test')
            
            # Should preserve duplicates as-is
            self.assertEqual(len(test_category.keywords), 4)
            self.assertEqual(test_category.keywords.count('sad'), 3)
            self.assertIn('down', test_category.keywords)
        finally:
            Path(temp_file.name).unlink()


class TestResponseDatabaseErrorHandling(unittest.TestCase):
    """Test error handling in ResponseDatabase."""
    
    def test_file_not_found_error(self):
        """Test handling of file not found error."""
        with self.assertRaises(RuntimeError) as context:
            ResponseDatabase('nonexistent_file.json')
        
        self.assertIn("Error loading response database", str(context.exception))
    
    def test_invalid_json_error(self):
        """Test handling of invalid JSON error."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        temp_file.write("invalid json content {")
        temp_file.close()
        
        try:
            with self.assertRaises(RuntimeError) as context:
                ResponseDatabase(temp_file.name)
            
            self.assertIn("Invalid JSON", str(context.exception))
        finally:
            Path(temp_file.name).unlink()
    
    def test_missing_categories_section(self):
        """Test handling of missing categories section."""
        invalid_responses = {
            "schema_version": "1.0"
            # Missing categories section
        }
        
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(invalid_responses, temp_file)
        temp_file.close()
        
        try:
            with self.assertRaises(RuntimeError) as context:
                ResponseDatabase(temp_file.name)
            
            self.assertIn("missing 'categories' key", str(context.exception))
        finally:
            Path(temp_file.name).unlink()
    
    def test_invalid_category_structure(self):
        """Test handling of invalid category structure."""
        invalid_responses = {
            "schema_version": "1.0",
            "categories": {
                "invalid": {
                    # Missing required fields
                    "keywords": ["test"]
                    # Missing responses
                },
                "fallback": {
                    "keywords": [],
                    "responses": ["Fallback response"],
                    "furby_sounds": ["*chirp*"],
                    "furbish_phrases": []
                }
            }
        }
        
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(invalid_responses, temp_file)
        temp_file.close()
        
        try:
            with self.assertRaises(RuntimeError) as context:
                ResponseDatabase(temp_file.name)
            
            self.assertIn("missing required field", str(context.exception))
        finally:
            Path(temp_file.name).unlink()


if __name__ == '__main__':
    unittest.main()