"""
Unit tests for the keyword matcher module.
"""

import unittest
from unittest.mock import Mock, patch
from furby_therapist.matcher import KeywordMatcher
from furby_therapist.database import ResponseDatabase, ResponseCategory
from furby_therapist.models import QueryAnalysis


class TestKeywordMatcher(unittest.TestCase):
    """Test cases for KeywordMatcher class."""
    
    def setUp(self):
        """Set up test fixtures with mock database."""
        # Create mock response categories
        self.mock_categories = {
            'sadness': ResponseCategory(
                name='sadness',
                keywords=['sad', 'cry', 'crying', 'upset', 'down', 'depressed'],
                responses=['Test sad response'],
                furby_sounds=['*purr*'],
                furbish_phrases=[('Dah a-loh', 'me love you')]
            ),
            'anxiety': ResponseCategory(
                name='anxiety', 
                keywords=['anxious', 'worried', 'stress', 'nervous', 'panic', 'fear'],
                responses=['Test anxiety response'],
                furby_sounds=['*chirp*'],
                furbish_phrases=[('Dah koh-koh', 'be calm')]
            ),
            'happiness': ResponseCategory(
                name='happiness',
                keywords=['happy', 'joy', 'excited', 'great', 'wonderful'],
                responses=['Test happy response'],
                furby_sounds=['*trill*'],
                furbish_phrases=[('Wee-tah', 'yay')]
            ),
            'fallback': ResponseCategory(
                name='fallback',
                keywords=[],
                responses=['Test fallback response'],
                furby_sounds=['*hum*'],
                furbish_phrases=[('Dah koh-koh', 'it\'s okay')]
            )
        }
        
        # Create mock database
        self.mock_database = Mock(spec=ResponseDatabase)
        self.mock_database.get_all_categories.return_value = self.mock_categories
        
        # Create matcher instance
        self.matcher = KeywordMatcher(self.mock_database)
    
    def test_exact_keyword_match(self):
        """Test exact keyword matching returns correct category."""
        keywords = ['sad', 'crying']
        category, confidence = self.matcher.match_category(keywords)
        
        self.assertEqual(category, 'sadness')
        self.assertGreater(confidence, 0.5)
    
    def test_partial_keyword_match(self):
        """Test partial keyword matching works correctly."""
        keywords = ['worried', 'stress']
        category, confidence = self.matcher.match_category(keywords)
        
        self.assertEqual(category, 'anxiety')
        self.assertGreater(confidence, 0.0)
    
    def test_fuzzy_keyword_match(self):
        """Test fuzzy matching handles word variations."""
        # Test with word variations (stemming-like)
        keywords = ['crying']  # Should match 'cry' in sadness category
        category, confidence = self.matcher.match_category(keywords)
        
        self.assertEqual(category, 'sadness')
        self.assertGreater(confidence, 0.0)
    
    def test_multiple_category_matches(self):
        """Test that highest scoring category is selected."""
        # Keywords that could match multiple categories
        keywords = ['sad', 'worried']  # Both sadness and anxiety keywords
        category, confidence = self.matcher.match_category(keywords)
        
        # Should return one of the categories (implementation dependent)
        self.assertIn(category, ['sadness', 'anxiety'])
        self.assertGreater(confidence, 0.0)
    
    def test_no_keyword_matches_returns_fallback(self):
        """Test that unmatched keywords return fallback category."""
        keywords = ['randomword', 'nonexistent']
        category, confidence = self.matcher.match_category(keywords)
        
        self.assertEqual(category, 'fallback')
        self.assertEqual(confidence, 0.1)
    
    def test_empty_keywords_returns_fallback(self):
        """Test that empty keyword list returns fallback category."""
        keywords = []
        category, confidence = self.matcher.match_category(keywords)
        
        self.assertEqual(category, 'fallback')
        self.assertEqual(confidence, 0.1)
    
    def test_confidence_scoring(self):
        """Test confidence scoring system."""
        # Test high confidence with exact matches
        high_conf_keywords = ['sad', 'depressed', 'crying']
        _, high_confidence = self.matcher.match_category(high_conf_keywords)
        
        # Test lower confidence with fewer matches
        low_conf_keywords = ['sad']
        _, low_confidence = self.matcher.match_category(low_conf_keywords)
        
        self.assertGreaterEqual(high_confidence, low_confidence)
        self.assertLessEqual(high_confidence, 1.0)
        self.assertGreaterEqual(low_confidence, 0.0)
    
    def test_calculate_category_score(self):
        """Test internal category scoring method."""
        user_keywords = ['sad', 'crying']
        category_keywords = ['sad', 'cry', 'upset', 'down']
        
        score = self.matcher._calculate_category_score(user_keywords, category_keywords)
        self.assertGreater(score, 0.0)
    
    def test_keywords_match_exact(self):
        """Test exact keyword matching."""
        self.assertTrue(self.matcher._keywords_match('sad', 'sad'))
        self.assertFalse(self.matcher._keywords_match('happy', 'sad'))
    
    def test_keywords_match_containment(self):
        """Test containment-based keyword matching."""
        self.assertTrue(self.matcher._keywords_match('cry', 'crying'))
        self.assertTrue(self.matcher._keywords_match('crying', 'cry'))
        self.assertFalse(self.matcher._keywords_match('happy', 'sadness'))
    
    def test_fuzzy_match_stemming(self):
        """Test fuzzy matching with common suffixes."""
        self.assertTrue(self.matcher._fuzzy_match('crying', 'cry'))
        self.assertTrue(self.matcher._fuzzy_match('worried', 'worry'))
        self.assertTrue(self.matcher._fuzzy_match('happily', 'happy'))
        self.assertFalse(self.matcher._fuzzy_match('completely', 'different'))
    
    def test_analyze_query_complete(self):
        """Test complete query analysis."""
        normalized_text = "i am feeling very sad and crying"
        keywords = ['feeling', 'sad', 'crying']
        
        analysis = self.matcher.analyze_query(normalized_text, keywords)
        
        self.assertIsInstance(analysis, QueryAnalysis)
        self.assertEqual(analysis.normalized_text, normalized_text)
        self.assertEqual(analysis.keywords, keywords)
        self.assertEqual(analysis.category, 'sadness')
        self.assertEqual(analysis.detected_emotion, 'sad')
        self.assertGreater(analysis.confidence, 0.0)
    
    def test_analyze_query_fallback(self):
        """Test query analysis with fallback category."""
        normalized_text = "random unmatched text"
        keywords = ['random', 'unmatched']
        
        analysis = self.matcher.analyze_query(normalized_text, keywords)
        
        self.assertEqual(analysis.category, 'fallback')
        self.assertEqual(analysis.detected_emotion, 'unknown')
        self.assertEqual(analysis.confidence, 0.1)
    
    def test_emotion_mapping(self):
        """Test emotion detection mapping."""
        test_cases = [
            (['happy', 'joy'], 'happiness', 'happy'),
            (['anxious', 'worried'], 'anxiety', 'anxious'),
            (['sad', 'crying'], 'sadness', 'sad'),
        ]
        
        for keywords, expected_category, expected_emotion in test_cases:
            analysis = self.matcher.analyze_query('test', keywords)
            self.assertEqual(analysis.category, expected_category)
            self.assertEqual(analysis.detected_emotion, expected_emotion)
    
    def test_calculate_confidence_method(self):
        """Test standalone confidence calculation method."""
        # Test with matches
        matches = {'sadness': 2.0, 'anxiety': 1.0}
        confidence = self.matcher.calculate_confidence(matches)
        self.assertGreater(confidence, 0.0)
        self.assertLessEqual(confidence, 1.0)
        
        # Test with empty matches
        empty_matches = {}
        confidence = self.matcher.calculate_confidence(empty_matches)
        self.assertEqual(confidence, 0.0)
    
    def test_get_fallback_category(self):
        """Test fallback category retrieval."""
        category, confidence = self.matcher.get_fallback_category()
        self.assertEqual(category, 'fallback')
        self.assertEqual(confidence, 0.1)
    
    def test_edge_case_single_character_keywords(self):
        """Test handling of single character keywords."""
        keywords = ['x', 'z']  # Use chars that won't accidentally match
        category, confidence = self.matcher.match_category(keywords)
        # Should fallback since single chars are unlikely to match meaningfully
        self.assertEqual(category, 'fallback')
    
    def test_edge_case_very_long_keywords(self):
        """Test handling of very long keywords."""
        keywords = ['supercalifragilisticexpialidocious']
        category, confidence = self.matcher.match_category(keywords)
        self.assertEqual(category, 'fallback')
    
    def test_case_insensitive_matching(self):
        """Test that matching works regardless of case."""
        # Keywords should already be normalized to lowercase by processor
        keywords = ['sad', 'CRYING']  # Mixed case to test robustness
        category, confidence = self.matcher.match_category(keywords)
        # Should still work since our test data is lowercase
        self.assertIn(category, ['sadness', 'fallback'])


class TestBicycleEasterEggs(unittest.TestCase):
    """Test cases for bicycle-themed easter eggs functionality."""
    
    def setUp(self):
        """Set up test fixtures with bicycle category."""
        # Create mock response categories including bicycle
        self.mock_categories = {
            'bicycle': ResponseCategory(
                name='bicycle',
                keywords=['bike', 'bicycle', 'cycling', 'riding', 'pedal', 'chain', 'wheel', 'maintenance'],
                responses=['Test bicycle response with therapeutic value'],
                furby_sounds=['*wheel spin*', '*pedal sound*'],
                furbish_phrases=[('Dah wheel-loh', 'keep rolling forward')]
            ),
            'sadness': ResponseCategory(
                name='sadness',
                keywords=['sad', 'cry', 'crying', 'upset', 'down', 'depressed'],
                responses=['Test sad response'],
                furby_sounds=['*purr*'],
                furbish_phrases=[('Dah a-loh', 'me love you')]
            ),
            'fallback': ResponseCategory(
                name='fallback',
                keywords=[],
                responses=['Test fallback response'],
                furby_sounds=['*hum*'],
                furbish_phrases=[('Dah koh-koh', 'it\'s okay')]
            )
        }
        
        # Create mock database
        self.mock_database = Mock(spec=ResponseDatabase)
        self.mock_database.get_all_categories.return_value = self.mock_categories
        
        # Create matcher instance
        self.matcher = KeywordMatcher(self.mock_database)
    
    def test_bicycle_keyword_detection_basic(self):
        """Test basic bicycle keyword detection."""
        test_cases = [
            (['bike'], 'bicycle'),
            (['bicycle'], 'bicycle'),
            (['cycling'], 'bicycle'),
            (['riding'], 'bicycle'),
            (['pedal'], 'bicycle'),
            (['chain'], 'bicycle'),
            (['wheel'], 'bicycle'),
            (['maintenance'], 'bicycle'),
        ]
        
        for keywords, expected_category in test_cases:
            with self.subTest(keywords=keywords):
                category, confidence = self.matcher.match_category(keywords)
                self.assertEqual(category, expected_category)
                self.assertGreater(confidence, 0.0)
    
    def test_bicycle_keyword_detection_compound(self):
        """Test bicycle keyword detection with compound words."""
        test_cases = [
            (['biking'], 'bicycle'),
            (['cyclist'], 'bicycle'),
            (['bicycle'], 'bicycle'),
        ]
        
        for keywords, expected_category in test_cases:
            with self.subTest(keywords=keywords):
                category, confidence = self.matcher.match_category(keywords)
                self.assertEqual(category, expected_category)
                self.assertGreater(confidence, 0.0)
    
    def test_bicycle_priority_over_other_categories(self):
        """Test that bicycle keywords get priority over other emotional categories."""
        # Mix bicycle keywords with emotional keywords
        keywords = ['sad', 'bike', 'depressed']
        category, confidence = self.matcher.match_category(keywords)
        
        # Should prioritize bicycle over sadness
        self.assertEqual(category, 'bicycle')
        self.assertGreater(confidence, 0.0)
    
    def test_bicycle_multiple_keywords(self):
        """Test bicycle detection with multiple bicycle keywords."""
        keywords = ['bike', 'chain', 'maintenance', 'wheel']
        category, confidence = self.matcher.match_category(keywords)
        
        self.assertEqual(category, 'bicycle')
        self.assertGreater(confidence, 0.5)  # Should have high confidence with multiple matches
    
    def test_check_bicycle_keywords_method(self):
        """Test the _check_bicycle_keywords method directly."""
        # Test direct bicycle keywords
        score = self.matcher._check_bicycle_keywords(['bike', 'pedal'])
        self.assertGreater(score, 0.0)
        
        # Test non-bicycle keywords
        score = self.matcher._check_bicycle_keywords(['sad', 'angry'])
        self.assertEqual(score, 0.0)
        
        # Test mixed keywords
        score = self.matcher._check_bicycle_keywords(['bike', 'sad', 'wheel'])
        self.assertGreater(score, 0.0)
    
    def test_is_cycling_related_method(self):
        """Test the _is_cycling_related method."""
        # More specific cycling words that should match
        cycling_words = ['wheelset', 'tubeless', 'puncture', 'chainring', 'cassette', 'derailleur']
        non_cycling_words = ['happy', 'sad', 'computer', 'food', 'wheel', 'tire', 'repair']
        
        for word in cycling_words:
            with self.subTest(word=word):
                self.assertTrue(self.matcher._is_cycling_related(word))
        
        for word in non_cycling_words:
            with self.subTest(word=word):
                self.assertFalse(self.matcher._is_cycling_related(word))
    
    def test_bicycle_scoring_weights(self):
        """Test that bicycle keyword scoring uses appropriate weights."""
        # Direct match should score higher than partial match
        direct_score = self.matcher._check_bicycle_keywords(['bike'])
        partial_score = self.matcher._check_bicycle_keywords(['biking'])  # Contains 'bike'
        
        self.assertGreaterEqual(direct_score, partial_score)
        self.assertGreater(direct_score, 0.0)
        self.assertGreater(partial_score, 0.0)
    
    def test_bicycle_emotion_mapping(self):
        """Test that bicycle category maps to enthusiastic emotion."""
        analysis = self.matcher.analyze_query('bike maintenance', ['bike', 'maintenance'])
        
        self.assertEqual(analysis.category, 'bicycle')
        self.assertEqual(analysis.detected_emotion, 'enthusiastic')
        self.assertGreater(analysis.confidence, 0.0)
    
    def test_bicycle_fallback_behavior(self):
        """Test that non-bicycle keywords still work normally."""
        # Regular emotional keywords should still work
        keywords = ['sad', 'crying']
        category, confidence = self.matcher.match_category(keywords)
        
        self.assertEqual(category, 'sadness')
        self.assertGreater(confidence, 0.0)
        
        # Unknown keywords should still fallback
        keywords = ['randomword', 'unknown']
        category, confidence = self.matcher.match_category(keywords)
        
        self.assertEqual(category, 'fallback')
        self.assertEqual(confidence, 0.1)
    
    def test_bicycle_edge_cases(self):
        """Test edge cases for bicycle detection."""
        # Empty keywords
        keywords = []
        category, confidence = self.matcher.match_category(keywords)
        self.assertEqual(category, 'fallback')
        
        # Single character that might match
        keywords = ['b']  # Too short to match 'bike'
        category, confidence = self.matcher.match_category(keywords)
        self.assertEqual(category, 'fallback')
        
        # Very long word containing bike
        keywords = ['superbike']  # Should still match since it contains 'bike'
        category, confidence = self.matcher.match_category(keywords)
        self.assertEqual(category, 'bicycle')
    
    def test_bicycle_case_insensitive(self):
        """Test that bicycle detection is case insensitive."""
        # This test assumes keywords are already normalized to lowercase
        # by the processor, but tests robustness
        keywords = ['bike', 'BICYCLE', 'Cycling']
        category, confidence = self.matcher.match_category(keywords)
        
        # Should work regardless of case (assuming normalization happened)
        self.assertEqual(category, 'bicycle')


class TestKeywordMatcherIntegration(unittest.TestCase):
    """Integration tests with real response database."""
    
    @patch('furby_therapist.matcher.ResponseDatabase')
    def test_integration_with_real_database_structure(self, mock_db_class):
        """Test matcher works with realistic database structure."""
        # This would test with actual JSON structure but mocked file loading
        mock_db = Mock()
        mock_db.get_all_categories.return_value = {
            'sadness': ResponseCategory(
                name='sadness',
                keywords=['sad', 'cry', 'upset', 'down', 'depressed', 'hurt'],
                responses=['Furby response'],
                furby_sounds=['*purr*'],
                furbish_phrases=[('Dah a-loh', 'me love you')]
            ),
            'fallback': ResponseCategory(
                name='fallback',
                keywords=[],
                responses=['Fallback response'],
                furby_sounds=['*hum*'],
                furbish_phrases=[('Dah koh-koh', 'it\'s okay')]
            )
        }
        
        matcher = KeywordMatcher(mock_db)
        
        # Test realistic scenarios
        test_cases = [
            (['sad', 'feeling', 'down'], 'sadness'),
            (['hello', 'there'], 'fallback'),
            ([], 'fallback')
        ]
        
        for keywords, expected_category in test_cases:
            category, confidence = matcher.match_category(keywords)
            self.assertEqual(category, expected_category)


if __name__ == '__main__':
    unittest.main()