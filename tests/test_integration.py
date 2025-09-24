"""
Integration tests for the complete Furby Therapist pipeline.
Tests end-to-end query processing from CLI input to Furby response.
"""

import unittest
import json
import tempfile
import os
from unittest.mock import patch, MagicMock

from furby_therapist.cli import FurbyTherapistCLI
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
    
    def test_complete_pipeline_bicycle_easter_egg(self):
        """Test complete pipeline with bicycle easter egg."""
        query = "I love riding my bicycle in the morning"
        response = self.cli.process_single_query(query)
        
        self.assertIn("💜 Furby says:", response)
        # Should contain bicycle-themed content
        self.assertTrue(
            any(word in response.lower() for word in ['bike', 'cycle', 'pedal', 'wheel', 'chain'])
        )
    
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
        # Verify all components exist
        self.assertIsNotNone(self.cli.database)
        self.assertIsNotNone(self.cli.processor)
        self.assertIsNotNone(self.cli.matcher)
        self.assertIsNotNone(self.cli.response_engine)
        
        # Verify components have expected methods
        self.assertTrue(hasattr(self.cli.processor, 'process_query'))
        self.assertTrue(hasattr(self.cli.matcher, 'match_category'))
        self.assertTrue(hasattr(self.cli.response_engine, 'get_response'))
        self.assertTrue(hasattr(self.cli.database, 'get_category'))
    
    def test_pipeline_data_flow(self):
        """Test that data flows correctly through the pipeline."""
        query = "I'm worried about my future"
        
        # Process through each step manually to verify data flow
        analysis = self.cli.processor.process_query(query)
        self.assertIsInstance(analysis, QueryAnalysis)
        self.assertEqual(analysis.original_text, query)
        self.assertGreater(len(analysis.keywords), 0)
        
        # Match category
        category, confidence = self.cli.matcher.match_category(analysis.keywords)
        self.assertIsInstance(category, str)
        self.assertIsInstance(confidence, float)
        self.assertGreaterEqual(confidence, 0.0)
        self.assertLessEqual(confidence, 1.0)
        
        # Generate response
        furby_response = self.cli.response_engine.get_response(category, analysis.detected_emotion)
        self.assertIsInstance(furby_response, FurbyResponse)
        self.assertIsInstance(furby_response.formatted_output, str)
        self.assertGreater(len(furby_response.formatted_output), 0)
    
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


class TestErrorHandlingIntegration(unittest.TestCase):
    """Test error handling in the integrated system."""
    
    def test_missing_database_file(self):
        """Test behavior when response database file is missing."""
        # Test with a non-existent file path
        with patch('furby_therapist.cli.ResponseDatabase') as mock_db:
            mock_db.side_effect = FileNotFoundError("Response database file not found")
            
            # Should handle the error gracefully during initialization
            with self.assertRaises(SystemExit):
                FurbyTherapistCLI()
    
    def test_corrupted_database_file(self):
        """Test behavior when response database file is corrupted."""
        with patch('furby_therapist.cli.ResponseDatabase') as mock_db:
            mock_db.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
            
            # Should handle the error gracefully during initialization
            with self.assertRaises(SystemExit):
                FurbyTherapistCLI()
    
    def test_component_failure_recovery(self):
        """Test that the system recovers gracefully from component failures."""
        cli = FurbyTherapistCLI()
        
        # Mock a component to fail during processing
        with patch.object(cli.processor, 'process_query') as mock_process:
            mock_process.side_effect = Exception("Processing failed")
            
            response = cli.process_single_query("test query")
            
            # Should get an error response but not crash
            self.assertIn("💜 Furby says:", response)
            self.assertIn("hiccup", response.lower())


class TestCLIModeIntegration(unittest.TestCase):
    """Test CLI mode integration."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.cli = FurbyTherapistCLI()
    
    def test_single_query_mode_integration(self):
        """Test single query mode works end-to-end."""
        query = "I need some encouragement"
        
        # This should work without throwing exceptions
        response = self.cli.process_single_query(query)
        
        self.assertIn("💜 Furby says:", response)
        self.assertGreater(len(response.strip()), 20)
    
    def test_format_response_output(self):
        """Test response output formatting."""
        test_response = "This is a test response *chirp*"
        formatted = self.cli.format_response_output(test_response)
        
        self.assertIn("💜 Furby says:", formatted)
        self.assertIn(test_response, formatted)
    
    def test_signal_handler_setup(self):
        """Test that signal handlers can be set up without errors."""
        # Should not raise any exceptions
        self.cli.setup_signal_handlers()
    
    def test_interactive_mode_flag(self):
        """Test interactive mode flag management."""
        # Initially should be False
        self.assertFalse(self.cli._interactive_mode_active)
        
        # Should be able to set it
        self.cli._interactive_mode_active = True
        self.assertTrue(self.cli._interactive_mode_active)


if __name__ == '__main__':
    unittest.main()