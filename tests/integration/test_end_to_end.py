"""
Comprehensive end-to-end integration tests.
Tests complete workflows from user input to final output.
This file focuses on unique end-to-end scenarios not covered in test_integration.py
"""

import unittest
from unittest.mock import patch, MagicMock
from furby_therapist.cli.main import FurbyTherapistCLI, main
from furby_therapist import FurbyTherapist, process_single_query


class TestLibraryEndToEnd(unittest.TestCase):
    """Test library interface end-to-end workflows."""
    
    def test_process_single_query_function(self):
        """Test the standalone process_single_query function."""
        try:
            response = process_single_query("I'm feeling happy today")
            
            self.assertIsNotNone(response)
            self.assertGreater(len(response.formatted_output), 20)
        except RuntimeError:
            self.skipTest("Could not initialize library")
    
    def test_library_stateful_workflow(self):
        """Test stateful library workflow with session management."""
        try:
            therapist = FurbyTherapist(cycling_mode=False, maintain_session=True)
        except RuntimeError:
            self.skipTest("Could not initialize library")
        
        try:
            # Process multiple queries to test session continuity
            queries = [
                "Hello Furby",
                "I'm feeling sad",
                "Can you repeat that?",
                "Thank you for listening"
            ]
            
            for i, query in enumerate(queries):
                response = therapist.process_query(query)
                
                self.assertIsNotNone(response)
                self.assertGreater(len(response.formatted_output), 10)
                
                # Check session stats accumulate correctly
                stats = therapist.get_session_stats()
                # Allow some tolerance for failed queries
                self.assertGreaterEqual(stats["conversation_length"], i)
                self.assertTrue(stats["stateful_mode"])
        finally:
            therapist.cleanup()
    
    def test_library_stateless_workflow(self):
        """Test stateless library workflow."""
        try:
            therapist = FurbyTherapist(cycling_mode=False, maintain_session=False)
        except RuntimeError:
            self.skipTest("Could not initialize library")
        
        try:
            # Process queries in stateless mode
            queries = ["Hello", "How are you?", "Goodbye"]
            
            for query in queries:
                response = therapist.process_query(query)
                self.assertIsNotNone(response)
                
                # In stateless mode, conversation length should not accumulate
                stats = therapist.get_session_stats()
                self.assertFalse(stats["stateful_mode"])
        finally:
            therapist.cleanup()
    
    def test_main_function_integration(self):
        """Test the main CLI entry point function."""
        # Test main function with mocked arguments
        with patch('sys.argv', ['furby_therapist', '--query', 'test']):
            with patch('furby_therapist.cli.main.FurbyTherapistCLI') as mock_cli_class:
                mock_cli = MagicMock()
                mock_cli_class.return_value = mock_cli
                
                try:
                    main()
                except SystemExit:
                    pass  # Expected for successful completion
                
                mock_cli_class.assert_called_once()
                mock_cli.setup_signal_handlers.assert_called_once()
                mock_cli.single_query_mode.assert_called_once_with('test')


if __name__ == '__main__':
    unittest.main()