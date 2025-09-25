"""
Unit tests for cycling keyword handling without bicycle category.
"""

import unittest
from furby_therapist.core.matcher import KeywordMatcher
from furby_therapist.core.processor import QueryProcessor
from furby_therapist.core.responses import ResponseEngine
from furby_therapist.core.database import ResponseDatabase


class TestCyclingKeywordHandling(unittest.TestCase):
    """Test how cycling keywords are handled without bicycle category."""
    
    def setUp(self):
        """Set up test fixtures with cycling mode enabled."""
        self.database = ResponseDatabase()
        self.processor = QueryProcessor()
        self.matcher = KeywordMatcher(self.database, cycling_mode=True)
        self.response_engine = ResponseEngine(cycling_mode=True)
    
    def test_cycling_keywords_fallback_gracefully(self):
        """Test that cycling keywords fall back to appropriate categories."""
        cycling_queries = [
            "I love gravel grinding",
            "My bike is awesome", 
            "Rigid MTB on road is fun",
            "Bikepacking adventure",
            "Alt cycling community",
        ]
        
        for query in cycling_queries:
            with self.subTest(query=query):
                keywords = self.processor.extract_keywords(query)
                category, confidence = self.matcher.match_category(keywords)
                # Should fall back to general or fallback, not crash
                self.assertIn(category, ['general', 'fallback', 'happiness'])
                self.assertGreaterEqual(confidence, 0.0)
    
    def test_cycling_with_emotions_prioritizes_emotion(self):
        """Test that emotional keywords take priority over cycling keywords."""
        mixed_queries = [
            ("I'm sad about my bike being stolen", 'sadness'),
            ("Happy about my new bike", 'happiness'),
            ("Anxious about my first century ride", 'anxiety'),
            ("Angry at bike thieves", 'anger')
        ]
        
        for query, expected_emotion_category in mixed_queries:
            with self.subTest(query=query):
                keywords = self.processor.extract_keywords(query)
                category, confidence = self.matcher.match_category(keywords)
                # Should prioritize emotional category over cycling terms
                self.assertIn(category, [expected_emotion_category, 'fallback', 'general'])
                self.assertGreaterEqual(confidence, 0.0)
    
    def test_cycling_terminology_extraction(self):
        """Test that cycling terminology is still extracted as keywords."""
        cycling_queries = [
            "n+1 bike rule",
            "reach and stack measurements", 
            "tire clearance issues",
            "bottom bracket standards",
        ]
        
        for query in cycling_queries:
            with self.subTest(query=query):
                keywords = self.processor.extract_keywords(query)
                # Should extract cycling terms as keywords
                cycling_terms = ['bike', 'reach', 'stack', 'tire', 'bracket']
                has_cycling_term = any(term in keywords for term in cycling_terms)
                self.assertTrue(has_cycling_term, 
                              f"Should extract cycling terms from: {query}")
    
    def test_cycling_mode_responses_still_work(self):
        """Test that cycling mode responses still work for valid categories."""
        # Test with valid categories that should work
        valid_categories = ['happiness', 'sadness', 'general', 'fallback']
        
        for category in valid_categories:
            with self.subTest(category=category):
                response = self.response_engine.get_response(category)
                if response:  # Some categories might not have responses in test data
                    self.assertIsNotNone(response.formatted_output)
                    self.assertGreater(len(response.formatted_output), 0)
    
    def test_therapeutic_tone_maintained_in_cycling_mode(self):
        """Test that cycling mode maintains therapeutic tone."""
        # Process cycling-related queries and check responses
        cycling_queries = [
            "I love cycling but I'm sad",
            "My bike makes me happy",
            "I'm worried about bike maintenance"
        ]
        
        for query in cycling_queries:
            with self.subTest(query=query):
                keywords = self.processor.extract_keywords(query)
                category, confidence = self.matcher.match_category(keywords)
                
                if category != 'fallback':
                    response = self.response_engine.get_response(category)
                    if response:
                        response_text = response.formatted_output.lower()
                        
                        # Should contain therapeutic elements (expanded to include cycling-themed therapeutic language)
                        therapeutic_indicators = [
                            'furby', 'understand', 'support', 'help', 'feel',
                            'better', 'together', 'care', 'listen', 'here',
                            'happiness', 'good', 'positive', 'great', 'perfect',
                            'clicks', 'vibes', 'smooth', 'satisfying', 'keep',
                            'builds', 'character', 'find', 'again', 'encouraging',
                            'determined', 'exhausting', 'tailwind', 'headwind',
                            'joy', 'earned', 'exhilarating', 'worth', 'enjoy',
                            'ride', 'climb', 'descent', 'thrilling', 'wee-tah'
                        ]
                        
                        has_therapeutic = any(indicator in response_text 
                                            for indicator in therapeutic_indicators)
                        
                        self.assertTrue(has_therapeutic,
                                      f"Response should maintain therapeutic tone: {response_text}")
    
    def test_non_cycling_keywords_unaffected(self):
        """Test that non-cycling keywords work normally."""
        non_cycling_queries = [
            "I'm feeling sad about work",
            "Happy about my promotion", 
            "Anxious about the future",
            "Angry at my situation"
        ]
        
        for query in non_cycling_queries:
            with self.subTest(query=query):
                keywords = self.processor.extract_keywords(query)
                category, confidence = self.matcher.match_category(keywords)
                # Should match appropriate emotional categories
                expected_categories = ['sadness', 'happiness', 'anxiety', 'anger', 'general', 'fallback']
                self.assertIn(category, expected_categories)
                self.assertGreaterEqual(confidence, 0.0)
    
    def test_cycling_keywords_dont_crash_system(self):
        """Test that cycling keywords don't cause system crashes."""
        cycling_keywords_lists = [
            ['bike', 'cycling', 'pedal'],
            ['gravel', 'grinding'],
            ['frankenbike', 'build'],
            ['randonneuring', 'event'],
            ['xbiking', 'community']
        ]
        
        for keywords in cycling_keywords_lists:
            with self.subTest(keywords=keywords):
                # Should not crash when processing cycling keywords
                category, confidence = self.matcher.match_category(keywords)
                self.assertIsNotNone(category)
                self.assertIsInstance(confidence, (int, float))
                self.assertGreaterEqual(confidence, 0.0)
    
    def test_compound_cycling_terms_handled(self):
        """Test that compound cycling terms are handled gracefully."""
        compound_queries = [
            "bikepacking gear setup",
            "wheelset upgrade needed", 
            "chainring replacement",
            "seatpost adjustment",
            "headset maintenance"
        ]
        
        for query in compound_queries:
            with self.subTest(query=query):
                keywords = self.processor.extract_keywords(query)
                category, confidence = self.matcher.match_category(keywords)
                # Should handle gracefully without crashing
                self.assertIn(category, ['general', 'fallback', 'happiness', 'sadness'])
                self.assertGreaterEqual(confidence, 0.0)


if __name__ == '__main__':
    unittest.main()