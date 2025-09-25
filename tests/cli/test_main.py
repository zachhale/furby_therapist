"""
Unit tests for CLI main functionality.

Tests the command-line interface components including argument parsing,
interactive mode, and single query processing.
"""

import unittest
import sys
import io
from unittest.mock import patch, MagicMock
from furby_therapist.cli.main import FurbyTherapistCLI, create_argument_parser, main


class TestFurbyTherapistCLI(unittest.TestCase):
    """Test the main CLI functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.cli = None
    
    def tearDown(self):
        """Clean up after tests."""
        if self.cli and hasattr(self.cli, 'furby_therapist'):
            self.cli.furby_therapist.cleanup()
    
    @patch('furby_therapist.core.database.ResponseDatabase')
    def test_cli_initialization_standard_mode(self, mock_db):
        """Test CLI initializes correctly in standard mode."""
        # Mock the database to return test data
        mock_db.return_value.get_all_categories.return_value = {
            'fallback': MagicMock(keywords=[], responses=['test response'])
        }
        
        self.cli = FurbyTherapistCLI(cycling_mode=False)
        
        self.assertIsNotNone(self.cli.furby_therapist)
        self.assertFalse(self.cli.cycling_mode)
        self.assertFalse(self.cli.furby_therapist.is_cycling_mode())
    
    @patch('furby_therapist.core.database.ResponseDatabase')
    def test_cli_initialization_cycling_mode(self, mock_db):
        """Test CLI initializes correctly in cycling mode."""
        # Mock the database to return test data
        mock_db.return_value.get_all_categories.return_value = {
            'fallback': MagicMock(keywords=[], responses=['test response'])
        }
        
        self.cli = FurbyTherapistCLI(cycling_mode=True)
        
        self.assertIsNotNone(self.cli.furby_therapist)
        self.assertTrue(self.cli.cycling_mode)
        self.assertTrue(self.cli.furby_therapist.is_cycling_mode())
    
    @patch('furby_therapist.core.database.ResponseDatabase')
    def test_single_query_processing(self, mock_db):
        """Test single query processing."""
        # Mock the database to return test data
        mock_db.return_value.get_all_categories.return_value = {
            'fallback': MagicMock(keywords=[], responses=['test response'])
        }
        
        self.cli = FurbyTherapistCLI()
        
        # Capture stdout to test output
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.cli.single_query_mode("test query")
            output = mock_stdout.getvalue()
        
        self.assertIn("Furby says:", output)
        self.assertGreater(len(output.strip()), 10)
    
    @patch('furby_therapist.core.database.ResponseDatabase')
    def test_format_response_output(self, mock_db):
        """Test response formatting."""
        # Mock the database to return test data
        mock_db.return_value.get_all_categories.return_value = {
            'fallback': MagicMock(keywords=[], responses=['test response'])
        }
        
        self.cli = FurbyTherapistCLI()
        
        formatted = self.cli.format_response_output("test response")
        
        self.assertIn("💜 Furby says:", formatted)
        self.assertIn("test response", formatted)


class TestArgumentParser(unittest.TestCase):
    """Test the argument parser functionality."""
    
    def test_create_argument_parser(self):
        """Test argument parser creation."""
        parser = create_argument_parser()
        
        self.assertIsNotNone(parser)
        
        # Test default arguments (no arguments)
        args = parser.parse_args([])
        self.assertIsNone(args.query)
        self.assertFalse(args.bikes)
    
    def test_query_argument(self):
        """Test query argument parsing."""
        parser = create_argument_parser()
        
        args = parser.parse_args(['--query', 'test query'])
        self.assertEqual(args.query, 'test query')
        
        args = parser.parse_args(['-q', 'short query'])
        self.assertEqual(args.query, 'short query')
    
    def test_bikes_argument(self):
        """Test bikes flag parsing."""
        parser = create_argument_parser()
        
        args = parser.parse_args(['--bikes'])
        self.assertTrue(args.bikes)
    
    def test_combined_arguments(self):
        """Test combined arguments."""
        parser = create_argument_parser()
        
        args = parser.parse_args(['--bikes', '--query', 'cycling query'])
        self.assertTrue(args.bikes)
        self.assertEqual(args.query, 'cycling query')


class TestMainFunction(unittest.TestCase):
    """Test the main entry point function."""
    
    @patch('furby_therapist.cli.main.FurbyTherapistCLI')
    @patch('sys.argv', ['furby_therapist', '--query', 'test'])
    def test_main_single_query(self, mock_cli_class):
        """Test main function with single query."""
        mock_cli = MagicMock()
        mock_cli_class.return_value = mock_cli
        
        try:
            main()
        except SystemExit:
            pass  # Expected for successful completion
        
        mock_cli_class.assert_called_once_with(cycling_mode=False)
        mock_cli.setup_signal_handlers.assert_called_once()
        mock_cli.single_query_mode.assert_called_once_with('test')
    
    @patch('furby_therapist.cli.main.FurbyTherapistCLI')
    @patch('sys.argv', ['furby_therapist', '--bikes'])
    def test_main_interactive_cycling(self, mock_cli_class):
        """Test main function with cycling mode."""
        mock_cli = MagicMock()
        mock_cli_class.return_value = mock_cli
        
        try:
            main()
        except SystemExit:
            pass  # Expected for successful completion
        
        mock_cli_class.assert_called_once_with(cycling_mode=True)
        mock_cli.setup_signal_handlers.assert_called_once()
        mock_cli.interactive_mode.assert_called_once()


if __name__ == '__main__':
    unittest.main()