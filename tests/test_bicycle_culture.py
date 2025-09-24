"""
Unit tests for expanded bicycle culture references and cycling community humor.
"""

import unittest
from furby_therapist.matcher import KeywordMatcher
from furby_therapist.processor import QueryProcessor
from furby_therapist.responses import ResponseEngine
from furby_therapist.database import ResponseDatabase


class TestBicycleCultureReferences(unittest.TestCase):
    """Test expanded bicycle culture references and cycling community humor."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.database = ResponseDatabase()
        self.matcher = KeywordMatcher(self.database)
        self.processor = QueryProcessor()
        self.engine = ResponseEngine()
    
    def test_alt_cycling_keywords(self):
        """Test detection of alternative cycling culture keywords."""
        alt_cycling_queries = [
            "I love gravel grinding",
            "My frankenbike is awesome", 
            "Rigid MTB on road is fun",
            "Bikepacking adventure",
            "Alt cycling community",
            "xbiking weird bikes",
            "The Radavist article",
            "Path Less Pedaled video",
            "constructeur frame building",
            "retrogrouch mindset"
        ]
        
        for query in alt_cycling_queries:
            with self.subTest(query=query):
                keywords = self.processor.extract_keywords(query)
                category, confidence = self.matcher.match_category(keywords)
                self.assertEqual(category, 'bicycle', 
                               f"Query '{query}' should match bicycle category")
                self.assertGreater(confidence, 0.15, 
                                 f"Query '{query}' should have decent confidence")
    
    def test_cycling_gear_debate_keywords(self):
        """Test detection of cycling gear debate keywords."""
        gear_debate_queries = [
            "clipless vs flats debate",
            "carbon vs steel frame",
            "tubeless tire setup",
            "tire pressure discussion",
            "vintage bike restoration",
            "bike geometry discussion",
            "reach and stack ratio",
            "chainstay length affects handling",
            "650b vs 700c wheels",
            "endurance vs aggressive geometry"
        ]
        
        for query in gear_debate_queries:
            with self.subTest(query=query):
                keywords = self.processor.extract_keywords(query)
                category, confidence = self.matcher.match_category(keywords)
                self.assertEqual(category, 'bicycle',
                               f"Query '{query}' should match bicycle category")
                self.assertGreater(confidence, 0.2,
                                 f"Query '{query}' should have some confidence")
    
    def test_cycling_magazine_references(self):
        """Test detection of cycling magazine and culture references."""
        magazine_queries = [
            "Bicycle Quarterly article",
            "randonneuring event",
            "Calling in Sick magazine",
            "bike messenger culture",
            "courier lifestyle"
        ]
        
        for query in magazine_queries:
            with self.subTest(query=query):
                keywords = self.processor.extract_keywords(query)
                category, confidence = self.matcher.match_category(keywords)
                self.assertEqual(category, 'bicycle',
                               f"Query '{query}' should match bicycle category")
    
    def test_xbiking_community_keywords(self):
        """Test detection of r/xbiking community specific terms."""
        xbiking_queries = [
            "weird bike build",
            "frankenbike project", 
            "rigid mountain bike",
            "xbiking community",
            "alternative cycling"
        ]
        
        for query in xbiking_queries:
            with self.subTest(query=query):
                keywords = self.processor.extract_keywords(query)
                category, confidence = self.matcher.match_category(keywords)
                self.assertEqual(category, 'bicycle',
                               f"Query '{query}' should match bicycle category")
    
    def test_bicycle_culture_responses_contain_references(self):
        """Test that bicycle responses contain cycling culture references."""
        # Get multiple bicycle responses to check variety
        responses = []
        for _ in range(10):
            response = self.engine.get_response('bicycle')
            responses.append(response.formatted_output.lower())
        
        # Check that we have variety in responses
        unique_responses = set(responses)
        self.assertGreater(len(unique_responses), 3, 
                          "Should have variety in bicycle responses")
        
        # Check for cycling culture terms across all responses
        culture_terms = [
            'gravel', 'frankenbike', 'rigid', 'alt cycling', 'xbiking',
            'clipless', 'flats', 'carbon', 'steel', 'tubeless', 
            'randonneuring', 'messenger', 'quarterly', 'calling in sick',
            'tire pressure', 'strava', 'geometry', 'reach', 'stack',
            'chainstay', 'wheelbase', 'bb drop', 'trail', 'constructeur',
            'radavist', 'retrogrouch', 'monster cross', 'endurance'
        ]
        
        found_terms = set()
        for response in responses:
            for term in culture_terms:
                if term in response:
                    found_terms.add(term)
        
        # Should find at least some culture terms in the responses
        self.assertGreater(len(found_terms), 0,
                          "Bicycle responses should contain cycling culture references")
    
    def test_therapeutic_tone_maintained(self):
        """Test that cycling culture responses maintain therapeutic tone."""
        # Get several bicycle responses
        for _ in range(5):
            response = self.engine.get_response('bicycle')
            response_text = response.formatted_output.lower()
            
            # Should contain supportive/therapeutic language
            therapeutic_indicators = [
                'furby', 'me think', 'me love', 'believe', 'support',
                'understand', 'help', 'teach', 'learn', 'grow', 'heal',
                'care', 'beautiful', 'strength', 'resilience', 'balance',
                'forward', 'progress', 'journey', 'patience', 'therapy',
                'therapeutic', 'best', 'sometimes', 'wisdom', 'trust',
                'process', 'character', 'soul', 'adaptation', 'meditation',
                'affects', 'like', 'relationships', 'boundaries', 'stable',
                'handling', 'center', 'grounding', 'find', 'wise', 'thoughtful'
            ]
            
            has_therapeutic_tone = any(indicator in response_text 
                                    for indicator in therapeutic_indicators)
            self.assertTrue(has_therapeutic_tone,
                           f"Response should maintain therapeutic tone: {response_text}")
    
    def test_cycling_metaphors_for_therapy(self):
        """Test that bicycle responses include therapeutic cycling metaphors."""
        # Get multiple responses to check for metaphors
        responses = []
        for _ in range(8):
            response = self.engine.get_response('bicycle')
            responses.append(response.formatted_output.lower())
        
        # Look for therapeutic metaphors
        metaphor_indicators = [
            'balance', 'forward', 'uphill', 'downhill', 'journey', 'path',
            'pedal stroke', 'maintenance', 'gears', 'smooth', 'rough',
            'distance', 'progress', 'carry', 'baggage', 'navigation'
        ]
        
        found_metaphors = set()
        for response in responses:
            for metaphor in metaphor_indicators:
                if metaphor in response:
                    found_metaphors.add(metaphor)
        
        self.assertGreater(len(found_metaphors), 0,
                          "Should find therapeutic cycling metaphors in responses")
    
    def test_expanded_keyword_detection_accuracy(self):
        """Test that expanded keywords don't create false positives."""
        # Non-cycling queries that might accidentally match
        non_cycling_queries = [
            "I'm feeling sad and tired",
            "Pressure at work is high",
            "I'm anxious about tomorrow",
            "Need help with depression",
            "Feeling lonely today"
        ]
        
        for query in non_cycling_queries:
            with self.subTest(query=query):
                keywords = self.processor.extract_keywords(query)
                category, confidence = self.matcher.match_category(keywords)
                # These should NOT match bicycle category
                self.assertNotEqual(category, 'bicycle',
                                  f"Query '{query}' should not match bicycle category")
    
    def test_compound_cycling_terms(self):
        """Test detection of compound cycling terms."""
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
                self.assertEqual(category, 'bicycle',
                               f"Compound term query '{query}' should match bicycle")
    
    def test_cycling_culture_keyword_scoring(self):
        """Test that cycling culture keywords get appropriate scoring."""
        # Test specific culture terms
        culture_keywords = [
            ['gravel', 'grinding'],
            ['frankenbike', 'build'],
            ['randonneuring', 'event'],
            ['xbiking', 'community'],
            ['clipless', 'vs', 'flats']
        ]
        
        for keywords in culture_keywords:
            with self.subTest(keywords=keywords):
                score = self.matcher._check_bicycle_keywords(keywords)
                self.assertGreater(score, 0,
                                 f"Keywords {keywords} should get bicycle score")
    
    def test_bicycle_responses_include_furby_sounds(self):
        """Test that bicycle responses include appropriate Furby sounds."""
        # Get several responses and check for cycling-themed sounds
        cycling_sounds = [
            '*wheel spin*', '*pedal sound*', '*chain click*', '*spoke ping*',
            '*bell ring*', '*gear shift*', '*tire pump*', '*crunch sound*',
            '*chain rattle*', '*pannier rustle*', '*hub sound*', '*click-clack*',
            '*frame tap*', '*urban bell ding*', '*whoosh*', '*seal sound*',
            # Also check for sounds that are embedded in the response text
            '*gentle pedal sound*', '*thoughtful chain click*', '*happy spoke ping*',
            '*playful bell ring*', '*determined gear shift*', '*satisfying seal sound*',
            '*determined crunch sound*', '*sage pump sound*', '*motivational beep*'
        ]
        
        found_sounds = set()
        for _ in range(10):
            response = self.engine.get_response('bicycle')
            response_text = response.formatted_output
            
            for sound in cycling_sounds:
                if sound in response_text:
                    found_sounds.add(sound)
        
        # Should find at least some cycling-themed sounds
        self.assertGreater(len(found_sounds), 0,
                          "Should find cycling-themed Furby sounds in responses")


if __name__ == '__main__':
    unittest.main()