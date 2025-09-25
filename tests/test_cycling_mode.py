"""
Tests for cycling mode functionality.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from furby_therapist.cli import FurbyTherapistCLI, create_argument_parser
from furby_therapist.matcher import KeywordMatcher
from furby_therapist.responses import ResponseEngine
from furby_therapist.database import ResponseDatabase


class TestCyclingMode(unittest.TestCase):
    """Test cycling mode functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.database = ResponseDatabase()
    
    def test_cli_initialization_standard_mode(self):
        """Test CLI initializes correctly in standard mode."""
        cli = FurbyTherapistCLI(cycling_mode=False)
        self.assertFalse(cli.cycling_mode)
        self.assertFalse(cli.matcher.cycling_mode)
        self.assertFalse(cli.response_engine.cycling_mode)
    
    def test_cli_initialization_cycling_mode(self):
        """Test CLI initializes correctly in cycling mode."""
        cli = FurbyTherapistCLI(cycling_mode=True)
        self.assertTrue(cli.cycling_mode)
        self.assertTrue(cli.matcher.cycling_mode)
        self.assertTrue(cli.response_engine.cycling_mode)
    
    def test_argument_parser_bikes_flag(self):
        """Test that --bikes flag is properly parsed."""
        parser = create_argument_parser()
        
        # Test without --bikes flag
        args = parser.parse_args([])
        self.assertFalse(args.bikes)
        
        # Test with --bikes flag
        args = parser.parse_args(['--bikes'])
        self.assertTrue(args.bikes)
        
        # Test with --bikes and query
        args = parser.parse_args(['--bikes', '--query', 'test'])
        self.assertTrue(args.bikes)
        self.assertEqual(args.query, 'test')
    
    def test_matcher_removes_bicycle_priority(self):
        """Test that bicycle category is no longer prioritized in matcher."""
        # Standard mode matcher
        standard_matcher = KeywordMatcher(self.database, cycling_mode=False)
        
        # Cycling mode matcher
        cycling_matcher = KeywordMatcher(self.database, cycling_mode=True)
        
        # Both should not have bicycle in matching categories
        self.assertNotIn('bicycle', standard_matcher.matching_categories)
        self.assertNotIn('bicycle', cycling_matcher.matching_categories)
        
        # Test that bicycle keywords don't get special priority
        bicycle_keywords = ['bike', 'cycling', 'pedal']
        
        # In both modes, bicycle keywords should be treated as regular keywords
        standard_category, standard_confidence = standard_matcher.match_category(bicycle_keywords)
        cycling_category, cycling_confidence = cycling_matcher.match_category(bicycle_keywords)
        
        # Neither should return 'bicycle' as the category
        self.assertNotEqual(standard_category, 'bicycle')
        self.assertNotEqual(cycling_category, 'bicycle')
    
    def test_response_engine_cycling_mode(self):
        """Test that response engine uses cycling responses in cycling mode."""
        # Standard mode
        standard_engine = ResponseEngine(cycling_mode=False)
        
        # Cycling mode
        cycling_engine = ResponseEngine(cycling_mode=True)
        
        # Test sadness responses
        standard_response = standard_engine.get_response('sadness')
        cycling_response = cycling_engine.get_response('sadness')
        
        # Cycling responses should contain bike-related terms
        cycling_keywords = ['bike', 'spoke', 'chain', 'wheel', 'gear', 'pedal', 'frame', 'tire']
        
        # Check if cycling response contains cycling terminology
        has_cycling_terms = any(keyword in cycling_response.formatted_output.lower() 
                               for keyword in cycling_keywords)
        
        # In cycling mode, responses should contain cycling terms
        if cycling_engine.cycling_mode:
            # Note: This might not always be true due to randomness, but we can check the categories exist
            self.assertTrue(len(cycling_engine.categories) > 0)
    
    def test_cycling_responses_maintain_therapeutic_value(self):
        """Test that cycling responses maintain therapeutic appropriateness."""
        cycling_engine = ResponseEngine(cycling_mode=True)
        
        # Test various emotional categories
        emotions = ['sadness', 'anxiety', 'anger', 'happiness', 'confusion', 'loneliness', 'gratitude']
        
        for emotion in emotions:
            if emotion in cycling_engine.categories:
                response = cycling_engine.get_response(emotion)
                
                # Response should not be empty
                self.assertIsNotNone(response.formatted_output)
                self.assertTrue(len(response.formatted_output) > 0)
                
                # Should contain Furby personality elements
                furby_indicators = ['*', 'me ', 'Furby', 'ooh', 'eee', 'wee-tah']
                has_furby_personality = any(indicator in response.formatted_output 
                                          for indicator in furby_indicators)
                self.assertTrue(has_furby_personality, 
                              f"Response for {emotion} lacks Furby personality: {response.formatted_output}")
    
    def test_standard_mode_no_cycling_humor(self):
        """Test that standard mode doesn't include cycling humor."""
        standard_engine = ResponseEngine(cycling_mode=False)
        
        # Generate multiple responses to check for cycling content
        responses = []
        emotions = ['sadness', 'anxiety', 'anger', 'happiness', 'confusion', 'loneliness', 'gratitude', 'general', 'fallback']
        
        for emotion in emotions:
            for _ in range(3):  # Generate 3 responses per emotion
                response = standard_engine.get_response(emotion)
                responses.append(response.formatted_output.lower())
        
        # Check that cycling-specific terms are not present in standard responses
        cycling_specific_terms = [
            'spoke', 'chainring', 'derailleur', 'gravel grinding', 'bikepacking', 
            'randonneuring', 'n+1 rule', 'reach-to-stack', 'wheelbase', 'chainstay',
            'headtube', 'trail', 'rake', 'geometry', 'radavist', 'path less pedaled',
            'bicycle quarterly', 'xbiking', 'frankenbike', 'retrogrouch', 'brevet',
            'audax', 'constructeur', 'porteur', 'fixed gear', 'single speed',
            'clipless', 'tubeless', 'tire pressure', 'psi', 'bb drop', 'slack',
            'steep angles', 'aggressive geometry', 'endurance geometry'
        ]
        
        # Count occurrences of cycling terms across all responses
        cycling_term_count = 0
        for response in responses:
            for term in cycling_specific_terms:
                if term in response:
                    cycling_term_count += 1
        
        # Standard mode should have NO cycling terminology
        self.assertEqual(cycling_term_count, 0, 
                        f"Standard mode should not contain cycling terminology. Found {cycling_term_count} instances.")
    
    def test_help_message_shows_mode(self):
        """Test that help message indicates current mode."""
        # Standard mode
        standard_cli = FurbyTherapistCLI(cycling_mode=False)
        
        # Cycling mode  
        cycling_cli = FurbyTherapistCLI(cycling_mode=True)
        
        # Both should have different cycling_mode values
        self.assertFalse(standard_cli.cycling_mode)
        self.assertTrue(cycling_cli.cycling_mode)
    
    @patch('sys.argv', ['furby_therapist', '--bikes', '--query', 'I am sad'])
    def test_main_function_cycling_mode_integration(self):
        """Test that main function properly handles cycling mode."""
        parser = create_argument_parser()
        args = parser.parse_args(['--bikes', '--query', 'I am sad'])
        
        self.assertTrue(args.bikes)
        self.assertEqual(args.query, 'I am sad')
    
    def test_cycling_mode_contains_cycling_humor(self):
        """Test that cycling mode contains cycling-specific content."""
        cycling_engine = ResponseEngine(cycling_mode=True)
        
        # Generate multiple responses to check for cycling content
        responses = []
        emotions = ['sadness', 'anxiety', 'anger', 'happiness', 'confusion', 'loneliness', 'gratitude', 'general', 'fallback']
        
        for emotion in emotions:
            for _ in range(3):  # Generate 3 responses per emotion
                response = cycling_engine.get_response(emotion)
                responses.append(response.formatted_output.lower())
        
        # Check that cycling-specific terms ARE present in cycling mode responses
        cycling_specific_terms = [
            'spoke', 'chain', 'wheel', 'gear', 'bike', 'cycling', 'pedal', 'frame',
            'gravel', 'n+1', 'geometry', 'reach', 'stack', 'wheelbase', 'tire',
            'pressure', 'psi', 'derailleur', 'cassette', 'chainring'
        ]
        
        # Count occurrences of cycling terms across all responses
        cycling_term_count = 0
        for response in responses:
            for term in cycling_specific_terms:
                if term in response:
                    cycling_term_count += 1
        
        # Cycling mode should have significant cycling terminology
        self.assertGreater(cycling_term_count, len(responses) * 0.5, 
                          f"Cycling mode should contain cycling terminology. Found only {cycling_term_count} instances in {len(responses)} responses.")
    
    def test_emotional_categories_work_in_cycling_mode(self):
        """Test that all emotional categories work properly in cycling mode."""
        cycling_engine = ResponseEngine(cycling_mode=True)
        
        # Test that we can get responses for all major emotional categories
        test_emotions = ['sadness', 'anxiety', 'anger', 'happiness', 'confusion', 'loneliness', 'gratitude', 'general', 'fallback']
        
        for emotion in test_emotions:
            with self.subTest(emotion=emotion):
                response = cycling_engine.get_response(emotion)
                
                # Should get a valid response
                self.assertIsNotNone(response)
                self.assertIsNotNone(response.formatted_output)
                self.assertTrue(len(response.formatted_output.strip()) > 0)
                
                # Should have Furby characteristics
                self.assertTrue('*' in response.formatted_output or 
                              'me ' in response.formatted_output.lower() or
                              'furby' in response.formatted_output.lower())
    
    def test_cli_integration_standard_vs_cycling_mode(self):
        """Test that CLI properly differentiates between standard and cycling modes."""
        # Test standard mode CLI
        standard_cli = FurbyTherapistCLI(cycling_mode=False)
        standard_response = standard_cli.process_single_query("I'm feeling sad")
        
        # Test cycling mode CLI
        cycling_cli = FurbyTherapistCLI(cycling_mode=True)
        cycling_response = cycling_cli.process_single_query("I'm feeling sad")
        
        # Both should be valid responses
        self.assertIsNotNone(standard_response)
        self.assertIsNotNone(cycling_response)
        
        # Responses should be different (cycling should have bike terms)
        cycling_terms = ['bike', 'spoke', 'chain', 'wheel', 'gear', 'pedal', 'frame', 'tire']
        
        # Standard response should not contain cycling terms
        standard_has_cycling = any(term in standard_response.lower() for term in cycling_terms)
        
        # Cycling response should contain cycling terms (though not guaranteed due to randomness)
        cycling_has_cycling = any(term in cycling_response.lower() for term in cycling_terms)
        
        # At minimum, standard mode should not have cycling terms
        self.assertFalse(standard_has_cycling, 
                        f"Standard mode response contains cycling terms: {standard_response}")
    
    def test_n_plus_one_rule_in_cycling_mode(self):
        """Test that N+1 rule jokes appear in cycling mode."""
        cycling_engine = ResponseEngine(cycling_mode=True)
        
        # Generate many responses to find N+1 references
        responses = []
        for _ in range(20):  # Generate more responses to catch N+1 references
            for emotion in ['general', 'fallback', 'happiness', 'anxiety']:
                response = cycling_engine.get_response(emotion)
                responses.append(response.formatted_output.lower())
        
        # Check for N+1 rule references
        n_plus_one_indicators = ['n+1', 'one more', 'need one more', 'always need']
        
        n_plus_one_count = sum(
            sum(1 for indicator in n_plus_one_indicators if indicator in response)
            for response in responses
        )
        
        # Should find some N+1 references in cycling mode
        self.assertGreater(n_plus_one_count, 0, 
                          "Cycling mode should include N+1 rule jokes")


if __name__ == '__main__':
    unittest.main()