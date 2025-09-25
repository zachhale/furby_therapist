"""
Integration tests for the complete Furby Therapist pipeline.
Tests end-to-end query processing from CLI input to Furby response.
"""

import unittest
import json
import tempfile
import os
from unittest.mock import patch, MagicMock, mock_open

from furby_therapist.cli.main import FurbyTherapistCLI
from furby_therapist.models import QueryAnalysis, FurbyResponse


class TestCompleteIntegration(unittest.TestCase):
    """Test the complete integration of all components."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.cli = FurbyTherapistCLI()
    
    def test_complete_pipeline_sadness(self):
        """Test complete pipeline with sadness query."""
        query = "I'm feeling really sad and lonely today"
        response = self.cli.process_single_query(query)
        
        # Verify we get a formatted response
        self.assertIn("💜 Furby says:", response)
        self.assertGreater(len(response.strip()), 50)  # Should be substantial
    
    def test_complete_pipeline_anxiety(self):
        """Test complete pipeline with anxiety query."""
        query = "I'm so anxious about my job interview tomorrow"
        response = self.cli.process_single_query(query)
        
        self.assertIn("💜 Furby says:", response)
        self.assertGreater(len(response.strip()), 50)
    
    @patch('furby_therapist.core.responses.open', new_callable=mock_open)
    @patch('furby_therapist.core.responses.Path')
    @patch('furby_therapist.core.database.ResponseDatabase')
    def test_complete_pipeline_cycling_keywords_handling(self, mock_db, mock_path, mock_file):
        """Test complete pipeline with cycling keywords handling."""
        # Mock file content
        test_responses = {"categories": {"fallback": {"keywords": [], "responses": ["test"], "furby_sounds": [], "furbish_phrases": []}}}
        mock_file.return_value.read.return_value = json.dumps(test_responses)
        mock_path.return_value.__truediv__.return_value = "test.json"
        
        # Mock database
        mock_db_instance = MagicMock()
        mock_db_instance.get_all_categories.return_value = {}
        mock_db.return_value = mock_db_instance
        
        # Test that cycling terms are handled gracefully in standard mode
        query = "I love riding my bicycle in the morning"
        standard_response = self.cli.process_single_query(query)
        
        self.assertIn("💜 Furby says:", standard_response)
        
        # Test that cycling mode can be initialized and handles cycling keywords
        cycling_cli = FurbyTherapistCLI(cycling_mode=True)
        cycling_response = cycling_cli.process_single_query(query)
        
        self.assertIn("💜 Furby says:", cycling_response)
    
    def test_complete_pipeline_cycling_culture_references(self):
        """Test complete pipeline with cycling culture references."""
        culture_queries = [
            "I love gravel grinding",
            "My frankenbike is awesome",
            "Bikepacking adventure planning",
            "Clipless vs flats debate"
        ]
        
        for query in culture_queries:
            with self.subTest(query=query):
                response = self.cli.process_single_query(query)
                self.assertIn("💜 Furby says:", response)
                # Should be a substantial response
                self.assertGreater(len(response.strip()), 50)
    
    def test_complete_pipeline_repeat_functionality(self):
        """Test complete pipeline with repeat functionality."""
        # First, make a regular query
        first_query = "I'm feeling happy today"
        first_response = self.cli.process_single_query(first_query)
        
        # Then ask for a repeat
        repeat_query = "repeat that please"
        repeat_response = self.cli.process_single_query(repeat_query)
        
        # Both should be valid responses
        self.assertIn("💜 Furby says:", first_response)
        self.assertIn("💜 Furby says:", repeat_response)
        
        # Repeat should be different (cleaner) but still substantial
        self.assertGreater(len(repeat_response.strip()), 30)
    
    def test_complete_pipeline_empty_input(self):
        """Test complete pipeline with empty input."""
        response = self.cli.process_single_query("")
        
        self.assertIn("💜 Furby says:", response)
        self.assertIn("listening", response.lower())
    
    def test_complete_pipeline_fallback_category(self):
        """Test complete pipeline with unrecognized input."""
        query = "xyz random nonsense words"
        response = self.cli.process_single_query(query)
        
        self.assertIn("💜 Furby says:", response)
        self.assertGreater(len(response.strip()), 30)
    
    def test_component_initialization(self):
        """Test that all components are properly initialized."""
        # Verify the library is initialized
        self.assertIsNotNone(self.cli.furby_therapist)
        
        # Verify library has expected methods
        self.assertTrue(hasattr(self.cli.furby_therapist, 'process_query'))
        self.assertTrue(hasattr(self.cli.furby_therapist, 'get_available_categories'))
        self.assertTrue(hasattr(self.cli.furby_therapist, 'get_good_morning_greeting'))
        self.assertTrue(hasattr(self.cli.furby_therapist, 'get_good_night_greeting'))
    
    def test_pipeline_data_flow(self):
        """Test that data flows correctly through the pipeline via library."""
        query = "I'm worried about my future"
        
        # Process through the library
        furby_response = self.cli.furby_therapist.process_query(query)
        self.assertIsInstance(furby_response, FurbyResponse)
        self.assertIsInstance(furby_response.formatted_output, str)
        self.assertGreater(len(furby_response.formatted_output), 0)
        
        # Verify the library provides expected functionality
        categories = self.cli.furby_therapist.get_available_categories()
        self.assertIsInstance(categories, list)
        self.assertGreater(len(categories), 0)
    
    def test_error_handling_integration(self):
        """Test error handling throughout the integrated pipeline."""
        # Test with None input
        response = self.cli.process_single_query(None)
        self.assertIn("💜 Furby says:", response)
        
        # Test with non-string input (should be handled gracefully)
        response = self.cli.process_single_query(123)
        self.assertIn("💜 Furby says:", response)
    
    def test_response_formatting_consistency(self):
        """Test that all responses are consistently formatted."""
        test_queries = [
            "I'm sad",
            "I'm happy", 
            "I'm confused",
            "I love my bike",
            "random words",
            ""
        ]
        
        for query in test_queries:
            response = self.cli.process_single_query(query)
            
            # All responses should have consistent formatting
            self.assertIn("💜 Furby says:", response)
            self.assertTrue(response.strip().endswith('\n') or len(response.strip()) > 0)


# Error handling integration tests moved to test_error_handling.py to reduce overlap


# CLI mode integration tests moved to test_end_to_end.py to reduce overlap


if __name__ == '__main__':
    unittest.main()