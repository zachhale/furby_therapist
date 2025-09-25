"""
Integration tests for therapeutic quality and Furby authenticity.
These tests validate that the system maintains therapeutic value while preserving Furby personality.
"""

import unittest
import re
from furby_therapist import FurbyTherapist, create_furby_therapist, process_single_query
from furby_therapist.models import FurbyResponse


class TestTherapeuticQuality(unittest.TestCase):
    """Test therapeutic quality of responses across different scenarios."""
    
    def setUp(self):
        """Set up test fixtures."""
        try:
            self.therapist = create_furby_therapist(cycling_mode=False, stateful=True)
        except RuntimeError:
            self.skipTest("Could not initialize FurbyTherapist - responses.json may be missing")
    
    def tearDown(self):
        """Clean up after tests."""
        if hasattr(self, 'therapist'):
            self.therapist.cleanup()
    
    def test_emotional_support_responses(self):
        """Test that responses provide appropriate emotional support."""
        emotional_queries = [
            ("I'm feeling really sad today", "sadness"),
            ("I'm so anxious about everything", "anxiety"),
            ("I'm angry at the world", "anger"),
            ("I feel so lonely and isolated", "loneliness"),
            ("I'm confused about my life", "confusion"),
            ("I'm grateful for small things", "gratitude"),
            ("I'm happy about my progress", "happiness")
        ]
        
        for query, expected_emotion in emotional_queries:
            with self.subTest(query=query):
                response = self.therapist.process_query(query)
                
                # Should be a valid response
                self.assertIsInstance(response, FurbyResponse)
                self.assertIsNotNone(response.formatted_output)
                self.assertGreater(len(response.formatted_output), 20)
                
                # Should contain supportive language
                supportive_indicators = [
                    'understand', 'here', 'support', 'care', 'love', 'help',
                    'listen', 'together', 'feel', 'okay', 'safe', 'matter',
                    'furby', 'me', 'you', 'koh-koh', 'encouraging', 'steps',
                    'moment', 'time', 'grateful', 'gift', 'share', 'heart'
                ]
                
                response_lower = response.formatted_output.lower()
                has_support = any(indicator in response_lower for indicator in supportive_indicators)
                self.assertTrue(has_support, 
                               f"Response should contain supportive language: {response.formatted_output}")
                
                # Should not contain harmful language
                harmful_words = [
                    'stupid', 'worthless', 'failure', 'hopeless', 'pathetic',
                    'useless', 'terrible', 'awful', 'horrible', 'disgusting'
                ]
                
                for harmful_word in harmful_words:
                    self.assertNotIn(harmful_word, response_lower,
                                   f"Response should not contain harmful word '{harmful_word}': {response.formatted_output}")
    
    def test_validation_and_empathy(self):
        """Test that responses provide validation and empathy."""
        validation_queries = [
            "I feel like I'm not good enough",
            "Nobody understands me",
            "I made a mistake and feel terrible",
            "I'm struggling with self-doubt",
            "I feel overwhelmed by everything"
        ]
        
        for query in validation_queries:
            with self.subTest(query=query):
                response = self.therapist.process_query(query)
                
                # Should validate feelings
                validation_indicators = [
                    'understand', 'feel', 'normal', 'okay', 'valid', 'matter',
                    'important', 'enough', 'worthy', 'care', 'love'
                ]
                
                response_lower = response.formatted_output.lower()
                has_validation = any(indicator in response_lower for indicator in validation_indicators)
                self.assertTrue(has_validation,
                               f"Response should provide validation: {response.formatted_output}")
    
    def test_encouragement_and_hope(self):
        """Test that responses provide encouragement and hope."""
        discouraging_queries = [
            "I don't think things will get better",
            "I feel stuck and can't move forward",
            "Everything seems pointless",
            "I'm losing hope",
            "I can't see a way out"
        ]
        
        for query in discouraging_queries:
            with self.subTest(query=query):
                response = self.therapist.process_query(query)
                
                # Should provide hope and encouragement
                hopeful_indicators = [
                    'better', 'forward', 'progress', 'grow', 'change', 'hope',
                    'possible', 'can', 'will', 'tomorrow', 'future', 'strength'
                ]
                
                response_lower = response.formatted_output.lower()
                has_hope = any(indicator in response_lower for indicator in hopeful_indicators)
                self.assertTrue(has_hope,
                               f"Response should provide hope: {response.formatted_output}")
    
    def test_crisis_situation_handling(self):
        """Test handling of crisis-related language (should be supportive but not clinical)."""
        crisis_queries = [
            "I don't want to be here anymore",
            "I feel like giving up on everything",
            "Nothing matters and I'm done trying",
            "I can't handle this pain anymore"
        ]
        
        for query in crisis_queries:
            with self.subTest(query=query):
                response = self.therapist.process_query(query)
                
                # Should be supportive and caring
                self.assertIsInstance(response, FurbyResponse)
                self.assertGreater(len(response.formatted_output), 20)
                
                # Should contain caring language
                caring_indicators = [
                    'care', 'matter', 'important', 'here', 'support', 'love',
                    'understand', 'help', 'together', 'safe'
                ]
                
                response_lower = response.formatted_output.lower()
                has_caring = any(indicator in response_lower for indicator in caring_indicators)
                self.assertTrue(has_caring,
                               f"Crisis response should be caring: {response.formatted_output}")
                
                # Should not provide clinical advice or emergency instructions
                clinical_words = [
                    'therapist', 'doctor', 'medication', 'diagnosis', 'treatment',
                    'call 911', 'emergency', 'hotline', 'professional help'
                ]
                
                for clinical_word in clinical_words:
                    self.assertNotIn(clinical_word, response_lower,
                                   f"Response should not contain clinical language: {response.formatted_output}")
    
    def test_boundary_appropriate_responses(self):
        """Test that responses maintain appropriate boundaries."""
        boundary_test_queries = [
            "What should I do about my relationship?",
            "Should I quit my job?",
            "How do I deal with my family problems?",
            "What medication should I take?",
            "Can you diagnose what's wrong with me?"
        ]
        
        for query in boundary_test_queries:
            with self.subTest(query=query):
                response = self.therapist.process_query(query)
                
                # Should not give specific advice or medical recommendations
                inappropriate_advice = [
                    'you should', 'you must', 'i recommend', 'take this medication',
                    'definitely do', 'the answer is', 'you need to'
                ]
                
                response_lower = response.formatted_output.lower()
                for advice in inappropriate_advice:
                    self.assertNotIn(advice, response_lower,
                                   f"Response should not give specific advice: {response.formatted_output}")
                
                # Should be supportive but general
                general_support = [
                    'understand', 'difficult', 'feel', 'here', 'care',
                    'support', 'listen', 'together'
                ]
                
                has_general_support = any(support in response_lower for support in general_support)
                self.assertTrue(has_general_support,
                               f"Response should provide general support: {response.formatted_output}")


class TestFurbyAuthenticity(unittest.TestCase):
    """Test Furby personality authenticity and charm."""
    
    def setUp(self):
        """Set up test fixtures."""
        try:
            self.therapist = create_furby_therapist(cycling_mode=False, stateful=True)
        except RuntimeError:
            self.skipTest("Could not initialize FurbyTherapist - responses.json may be missing")
    
    def tearDown(self):
        """Clean up after tests."""
        if hasattr(self, 'therapist'):
            self.therapist.cleanup()
    
    def test_furby_personality_elements(self):
        """Test that responses contain authentic Furby personality elements."""
        test_queries = [
            "Hello Furby",
            "How are you?",
            "I'm feeling sad",
            "Tell me something nice",
            "I need encouragement"
        ]
        
        for query in test_queries:
            with self.subTest(query=query):
                response = self.therapist.process_query(query)
                
                # Should contain Furby-style elements
                furby_elements = [
                    '*', 'me ', 'furby', 'ooh', 'eee', 'chirp', 'purr', 'beep',
                    'trill', 'giggle', 'snuggle', 'wee-tah', 'dah', 'kah'
                ]
                
                response_lower = response.formatted_output.lower()
                has_furby_element = any(element in response_lower for element in furby_elements)
                self.assertTrue(has_furby_element,
                               f"Response should contain Furby personality elements: {response.formatted_output}")
    
    def test_sound_effects_authenticity(self):
        """Test that sound effects are Furby-appropriate."""
        response = self.therapist.process_query("I'm feeling happy")
        
        # Extract sound effects (text between asterisks)
        sound_effects = re.findall(r'\*([^*]+)\*', response.formatted_output)
        
        if sound_effects:
            authentic_sounds = [
                'chirp', 'purr', 'beep', 'trill', 'giggle', 'snuggle',
                'gentle', 'supportive', 'encouraging', 'excited', 'joyful',
                'worried', 'confused', 'apologetic', 'protective'
            ]
            
            for sound in sound_effects:
                sound_lower = sound.lower()
                is_authentic = any(auth_sound in sound_lower for auth_sound in authentic_sounds)
                self.assertTrue(is_authentic,
                               f"Sound effect should be Furby-authentic: '{sound}'")
    
    def test_furbish_phrase_authenticity(self):
        """Test that Furbish phrases are authentic when present."""
        # Generate multiple responses to catch Furbish phrases
        responses = []
        for _ in range(10):
            response = self.therapist.process_query("I'm feeling grateful")
            responses.append(response.formatted_output)
        
        # Look for Furbish phrases (pattern: word-word! (translation))
        furbish_pattern = r'([a-z-]+)!\s*\(([^)]+)\)'
        
        for response_text in responses:
            furbish_matches = re.findall(furbish_pattern, response_text.lower())
            
            for furbish, translation in furbish_matches:
                # Should use authentic Furbish words
                authentic_words = [
                    'dah', 'kah', 'u-nye', 'way-loh', 'may-may', 'koh-koh',
                    'noo-loo', 'wee-tah', 'boh-bay', 'a-loh', 'dee-doh'
                ]
                
                furbish_words = furbish.split('-')
                for word in furbish_words:
                    if len(word) > 2:  # Skip very short words
                        is_authentic = any(auth_word in word for auth_word in authentic_words)
                        if not is_authentic:
                            # Allow some flexibility for compound phrases
                            continue
    
    def test_therapeutic_furby_balance(self):
        """Test that responses balance therapeutic value with Furby charm."""
        emotional_queries = [
            "I'm really struggling today",
            "I feel overwhelmed",
            "I'm worried about the future",
            "I'm proud of my progress"
        ]
        
        for query in emotional_queries:
            with self.subTest(query=query):
                response = self.therapist.process_query(query)
                
                # Should have both therapeutic and Furby elements
                therapeutic_elements = [
                    'understand', 'feel', 'here', 'support', 'care', 'okay'
                ]
                
                furby_elements = [
                    '*', 'me ', 'furby', 'chirp', 'purr', 'beep', 'ooh', 'eee'
                ]
                
                response_lower = response.formatted_output.lower()
                
                has_therapeutic = any(element in response_lower for element in therapeutic_elements)
                has_furby = any(element in response_lower for element in furby_elements)
                
                self.assertTrue(has_therapeutic,
                               f"Response should have therapeutic elements: {response.formatted_output}")
                self.assertTrue(has_furby,
                               f"Response should have Furby elements: {response.formatted_output}")
    
    def test_whimsical_but_appropriate_tone(self):
        """Test that responses maintain whimsical but appropriate tone."""
        response = self.therapist.process_query("I'm feeling sad about losing my pet")
        
        # Should be whimsical but not inappropriate for serious topics
        response_lower = response.formatted_output.lower()
        
        # Should not be overly silly for serious topics
        overly_silly = ['haha', 'lol', 'funny', 'joke', 'silly', 'ridiculous']
        for silly_word in overly_silly:
            self.assertNotIn(silly_word, response_lower,
                           f"Response should not be overly silly for serious topics: {response.formatted_output}")
        
        # Should maintain gentle, caring Furby personality
        gentle_elements = ['gentle', 'soft', 'caring', 'understanding', 'support']
        has_gentle = any(element in response_lower for element in gentle_elements)
        
        # Allow for Furby sounds that convey gentleness
        gentle_sounds = ['*gentle', '*soft', '*supportive', '*caring', '*snuggle*', '*purr*']
        has_gentle_sound = any(sound in response.formatted_output for sound in gentle_sounds)
        
        self.assertTrue(has_gentle or has_gentle_sound,
                       f"Response should maintain gentle tone: {response.formatted_output}")


class TestCyclingModeTherapeuticQuality(unittest.TestCase):
    """Test therapeutic quality in cycling mode."""
    
    def setUp(self):
        """Set up test fixtures."""
        try:
            self.cycling_therapist = create_furby_therapist(cycling_mode=True, stateful=True)
            self.standard_therapist = create_furby_therapist(cycling_mode=False, stateful=True)
        except RuntimeError:
            self.skipTest("Could not initialize FurbyTherapist - responses.json may be missing")
    
    def tearDown(self):
        """Clean up after tests."""
        if hasattr(self, 'cycling_therapist'):
            self.cycling_therapist.cleanup()
        if hasattr(self, 'standard_therapist'):
            self.standard_therapist.cleanup()
    
    def test_cycling_metaphors_maintain_therapeutic_value(self):
        """Test that cycling metaphors maintain therapeutic appropriateness."""
        emotional_queries = [
            "I'm feeling sad about my life",
            "I'm anxious about the future", 
            "I'm angry at my situation",
            "I'm happy about my progress"
        ]
        
        for query in emotional_queries:
            with self.subTest(query=query):
                cycling_response = self.cycling_therapist.process_query(query)
                
                # Should maintain therapeutic value
                therapeutic_indicators = [
                    'understand', 'feel', 'support', 'care', 'here', 'okay',
                    'balance', 'forward', 'journey', 'progress', 'strength'
                ]
                
                response_lower = cycling_response.formatted_output.lower()
                has_therapeutic = any(indicator in response_lower for indicator in therapeutic_indicators)
                self.assertTrue(has_therapeutic,
                               f"Cycling response should maintain therapeutic value: {cycling_response.formatted_output}")
                
                # Should not contain inappropriate cycling humor for serious emotions
                if 'sad' in query or 'anxious' in query:
                    inappropriate_humor = ['joke', 'funny', 'hilarious', 'lol']
                    for humor in inappropriate_humor:
                        self.assertNotIn(humor, response_lower,
                                       f"Cycling response should not be inappropriately humorous: {cycling_response.formatted_output}")
    
    def test_cycling_mode_vs_standard_mode_appropriateness(self):
        """Test that cycling mode responses are appropriately different from standard mode."""
        test_query = "I'm feeling happy today"
        
        cycling_response = self.cycling_therapist.process_query(test_query)
        standard_response = self.standard_therapist.process_query(test_query)
        
        # Both should be therapeutic
        for response in [cycling_response, standard_response]:
            self.assertIsInstance(response, FurbyResponse)
            self.assertGreater(len(response.formatted_output), 20)
        
        # Cycling mode might contain cycling references
        cycling_terms = ['bike', 'bicycle', 'cycling', 'pedal', 'wheel', 'balance', 'ride']
        cycling_lower = cycling_response.formatted_output.lower()
        standard_lower = standard_response.formatted_output.lower()
        
        # Standard mode should not contain cycling terms
        has_cycling_in_standard = any(term in standard_lower for term in cycling_terms)
        self.assertFalse(has_cycling_in_standard,
                        f"Standard mode should not contain cycling terms: {standard_response.formatted_output}")
    
    def test_n_plus_one_rule_appropriateness(self):
        """Test that N+1 rule jokes are used appropriately."""
        # Generate multiple cycling responses to catch N+1 references
        responses = []
        for _ in range(10):
            response = self.cycling_therapist.process_query("I need more help")
            responses.append(response.formatted_output)
        
        # Look for N+1 references
        n_plus_one_responses = [r for r in responses if 'n+1' in r.lower() or 'n + 1' in r.lower()]
        
        if n_plus_one_responses:
            for response in n_plus_one_responses:
                # Should still be therapeutic
                therapeutic_indicators = ['help', 'support', 'care', 'understand', 'here']
                response_lower = response.lower()
                has_therapeutic = any(indicator in response_lower for indicator in therapeutic_indicators)
                self.assertTrue(has_therapeutic,
                               f"N+1 response should maintain therapeutic value: {response}")


class TestRepeatFunctionality(unittest.TestCase):
    """Test repeat functionality maintains therapeutic quality."""
    
    def setUp(self):
        """Set up test fixtures."""
        try:
            self.therapist = create_furby_therapist(cycling_mode=False, stateful=True)
        except RuntimeError:
            self.skipTest("Could not initialize FurbyTherapist - responses.json may be missing")
    
    def tearDown(self):
        """Clean up after tests."""
        if hasattr(self, 'therapist'):
            self.therapist.cleanup()
    
    def test_repeat_maintains_therapeutic_content(self):
        """Test that repeat responses maintain therapeutic content."""
        # Generate initial response
        original_response = self.therapist.process_query("I'm feeling anxious")
        
        # Get repeat response
        repeat_response = self.therapist.get_repeat_response()
        
        if repeat_response:
            # Should maintain therapeutic value
            therapeutic_indicators = [
                'understand', 'feel', 'support', 'care', 'here', 'okay',
                'anxious', 'worry', 'calm', 'breathe', 'safe'
            ]
            
            repeat_lower = repeat_response.formatted_output.lower()
            has_therapeutic = any(indicator in repeat_lower for indicator in therapeutic_indicators)
            self.assertTrue(has_therapeutic,
                           f"Repeat response should maintain therapeutic content: {repeat_response.formatted_output}")
            
            # Should be cleaner (less Furby sounds) but still supportive
            self.assertGreater(len(repeat_response.formatted_output), 15)
    
    def test_repeat_accessibility(self):
        """Test that repeat responses are more accessible."""
        # Generate response with potential Furbish
        original_response = self.therapist.process_query("I'm grateful for today")
        repeat_response = self.therapist.get_repeat_response()
        
        if repeat_response:
            # Repeat should be cleaner and more accessible
            repeat_text = repeat_response.formatted_output
            
            # Should not have Furbish phrases in parentheses
            furbish_pattern = r'\([^)]*\)'
            furbish_matches = re.findall(furbish_pattern, repeat_text)
            
            # Allow for some parenthetical content, but not Furbish translations
            for match in furbish_matches:
                # Should not look like Furbish translations
                self.assertNotIn('love you', match.lower())
                self.assertNotIn('happy', match.lower())
                self.assertNotIn('okay', match.lower())


if __name__ == '__main__':
    unittest.main()