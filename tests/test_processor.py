"""
Unit tests for the query processor module.
"""

import unittest
from furby_therapist.processor import QueryProcessor, QueryAnalysis


class TestQueryProcessor(unittest.TestCase):
    """Test cases for QueryProcessor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.processor = QueryProcessor()
    
    def test_normalize_text_basic(self):
        """Test basic text normalization."""
        # Test lowercase conversion
        result = self.processor.normalize_text("HELLO WORLD")
        self.assertEqual(result, "hello world")
        
        # Test punctuation removal
        result = self.processor.normalize_text("Hello, world! How are you?")
        self.assertEqual(result, "hello world how are you")
        
        # Test whitespace normalization
        result = self.processor.normalize_text("hello    world   test")
        self.assertEqual(result, "hello world test")
    
    def test_normalize_text_contractions(self):
        """Test handling of contractions."""
        result = self.processor.normalize_text("I'm feeling sad, can't sleep")
        self.assertEqual(result, "im feeling sad cant sleep")
        
        result = self.processor.normalize_text("Don't worry, it's okay")
        self.assertEqual(result, "dont worry its okay")
    
    def test_normalize_text_edge_cases(self):
        """Test edge cases for text normalization."""
        # Empty string
        result = self.processor.normalize_text("")
        self.assertEqual(result, "")
        
        # Whitespace only
        result = self.processor.normalize_text("   ")
        self.assertEqual(result, "")
        
        # None input
        result = self.processor.normalize_text(None)
        self.assertEqual(result, "")
        
        # Special characters
        result = self.processor.normalize_text("@#$%^&*()")
        self.assertEqual(result, "")
    
    def test_extract_keywords_basic(self):
        """Test basic keyword extraction."""
        keywords = self.processor.extract_keywords("feeling sad today")
        self.assertEqual(keywords, ["feeling", "sad", "today"])
        
        keywords = self.processor.extract_keywords("very anxious about work")
        self.assertEqual(keywords, ["very", "anxious", "about", "work"])
    
    def test_extract_keywords_stop_words(self):
        """Test that stop words are filtered out."""
        keywords = self.processor.extract_keywords("i am feeling very sad and lonely")
        # 'i', 'am', 'and' should be filtered out as stop words
        self.assertEqual(keywords, ["feeling", "very", "sad", "lonely"])
        
        keywords = self.processor.extract_keywords("the cat is on the mat")
        # All words should be filtered out as stop words
        self.assertEqual(keywords, ["cat", "mat"])
    
    def test_extract_keywords_duplicates(self):
        """Test that duplicate keywords are removed."""
        keywords = self.processor.extract_keywords("sad sad very sad feeling")
        self.assertEqual(keywords, ["sad", "very", "feeling"])
    
    def test_extract_keywords_short_words(self):
        """Test that very short words are filtered out."""
        keywords = self.processor.extract_keywords("i am so sad to go")
        # 'so', 'to' should be filtered out (length <= 2)
        self.assertEqual(keywords, ["sad"])
    
    def test_extract_keywords_empty_input(self):
        """Test keyword extraction with empty input."""
        keywords = self.processor.extract_keywords("")
        self.assertEqual(keywords, [])
        
        keywords = self.processor.extract_keywords(None)
        self.assertEqual(keywords, [])
    
    def test_detect_emotion_sadness(self):
        """Test detection of sadness emotion."""
        emotion, confidence = self.processor.detect_emotion("feeling sad and depressed")
        self.assertEqual(emotion, "sadness")
        self.assertGreater(confidence, 0)
        
        emotion, confidence = self.processor.detect_emotion("crying lonely hurt")
        self.assertEqual(emotion, "sadness")
        self.assertGreater(confidence, 0)
    
    def test_detect_emotion_anxiety(self):
        """Test detection of anxiety emotion."""
        emotion, confidence = self.processor.detect_emotion("feeling anxious and worried")
        self.assertEqual(emotion, "anxiety")
        self.assertGreater(confidence, 0)
        
        emotion, confidence = self.processor.detect_emotion("scared nervous panic")
        self.assertEqual(emotion, "anxiety")
        self.assertGreater(confidence, 0)
    
    def test_detect_emotion_anger(self):
        """Test detection of anger emotion."""
        emotion, confidence = self.processor.detect_emotion("feeling angry and frustrated")
        self.assertEqual(emotion, "anger")
        self.assertGreater(confidence, 0)
        
        emotion, confidence = self.processor.detect_emotion("mad furious rage")
        self.assertEqual(emotion, "anger")
        self.assertGreater(confidence, 0)
    
    def test_detect_emotion_happiness(self):
        """Test detection of happiness emotion."""
        emotion, confidence = self.processor.detect_emotion("feeling happy and joyful")
        self.assertEqual(emotion, "happiness")
        self.assertGreater(confidence, 0)
        
        emotion, confidence = self.processor.detect_emotion("excited thrilled glad")
        self.assertEqual(emotion, "happiness")
        self.assertGreater(confidence, 0)
    
    def test_detect_emotion_confusion(self):
        """Test detection of confusion emotion."""
        emotion, confidence = self.processor.detect_emotion("feeling confused and lost")
        self.assertEqual(emotion, "confusion")
        self.assertGreater(confidence, 0)
        
        emotion, confidence = self.processor.detect_emotion("uncertain puzzled unclear")
        self.assertEqual(emotion, "confusion")
        self.assertGreater(confidence, 0)
    
    def test_detect_emotion_neutral(self):
        """Test neutral emotion detection."""
        emotion, confidence = self.processor.detect_emotion("hello how are you")
        self.assertEqual(emotion, "neutral")
        self.assertEqual(confidence, 0.0)
        
        emotion, confidence = self.processor.detect_emotion("")
        self.assertEqual(emotion, "neutral")
        self.assertEqual(confidence, 0.0)
    
    def test_detect_emotion_multiple_emotions(self):
        """Test emotion detection with multiple emotions present."""
        # Should return the emotion with highest score
        emotion, confidence = self.processor.detect_emotion("sad angry frustrated depressed")
        # Both sadness and anger keywords present, should pick the one with higher score
        self.assertIn(emotion, ["sadness", "anger"])
        self.assertGreater(confidence, 0)
    
    def test_detect_emotion_confidence_scoring(self):
        """Test that confidence scores are calculated correctly."""
        # More emotion words should give higher confidence
        emotion1, conf1 = self.processor.detect_emotion("sad")
        emotion2, conf2 = self.processor.detect_emotion("sad depressed")
        
        self.assertEqual(emotion1, "sadness")
        self.assertEqual(emotion2, "sadness")
        # More emotion keywords in shorter text should have higher confidence
        self.assertGreaterEqual(conf2, conf1)
    
    def test_process_query_complete_pipeline(self):
        """Test the complete query processing pipeline."""
        result = self.processor.process_query("I'm feeling really SAD and LONELY today!")
        
        self.assertEqual(result.original_text, "I'm feeling really SAD and LONELY today!")
        self.assertEqual(result.normalized_text, "im feeling really sad and lonely today")
        self.assertIn("sad", result.keywords)
        self.assertIn("lonely", result.keywords)
        self.assertIn("feeling", result.keywords)
        self.assertEqual(result.detected_emotion, "sadness")
        self.assertGreater(result.confidence, 0)
        self.assertEqual(result.category, "general")  # Default category
    
    def test_process_query_empty_input(self):
        """Test processing empty or invalid input."""
        result = self.processor.process_query("")
        
        self.assertEqual(result.original_text, "")
        self.assertEqual(result.normalized_text, "")
        self.assertEqual(result.keywords, [])
        self.assertEqual(result.detected_emotion, "neutral")
        self.assertEqual(result.confidence, 0.0)
    
    def test_process_query_complex_input(self):
        """Test processing complex real-world input."""
        query = "Hey there, I've been feeling super anxious about my job interview tomorrow. Can't sleep!"
        result = self.processor.process_query(query)
        
        self.assertEqual(result.original_text, query)
        self.assertIn("anxious", result.normalized_text)
        self.assertIn("anxious", result.keywords)
        self.assertIn("job", result.keywords)
        self.assertIn("interview", result.keywords)
        self.assertIn("sleep", result.keywords)
        self.assertEqual(result.detected_emotion, "anxiety")
        self.assertGreater(result.confidence, 0)
    
    def test_is_repeat_request_basic_keywords(self):
        """Test detection of basic repeat request keywords."""
        # Single repeat keywords
        self.assertTrue(self.processor.is_repeat_request("repeat"))
        self.assertTrue(self.processor.is_repeat_request("again"))
        self.assertTrue(self.processor.is_repeat_request("what"))
        self.assertTrue(self.processor.is_repeat_request("pardon"))
        self.assertTrue(self.processor.is_repeat_request("huh"))
        
        # Short phrases with repeat keywords
        self.assertTrue(self.processor.is_repeat_request("say again"))
        self.assertTrue(self.processor.is_repeat_request("what again"))
        self.assertTrue(self.processor.is_repeat_request("repeat that"))
    
    def test_is_repeat_request_common_phrases(self):
        """Test detection of common repeat request phrases."""
        repeat_phrases = [
            "say again",
            "what did you say",
            "repeat that",
            "come again",
            "didnt hear",
            "didnt understand", 
            "didnt catch",
            "say that again",
            "what was that",
            "pardon me",
            "excuse me",
            "sorry what"
        ]
        
        for phrase in repeat_phrases:
            with self.subTest(phrase=phrase):
                self.assertTrue(self.processor.is_repeat_request(phrase))
    
    def test_is_repeat_request_short_queries(self):
        """Test detection of short repeat-like queries."""
        # Very short queries with repeat keywords should be detected
        self.assertTrue(self.processor.is_repeat_request("what"))
        self.assertTrue(self.processor.is_repeat_request("huh"))
        self.assertTrue(self.processor.is_repeat_request("eh"))
        self.assertTrue(self.processor.is_repeat_request("sorry"))
        
        # Short queries with repeat keywords
        self.assertTrue(self.processor.is_repeat_request("what now"))
        self.assertTrue(self.processor.is_repeat_request("say what"))
        self.assertTrue(self.processor.is_repeat_request("come again"))
    
    def test_is_repeat_request_false_positives(self):
        """Test that non-repeat queries are not detected as repeats."""
        # Regular queries should not be detected as repeats
        self.assertFalse(self.processor.is_repeat_request("i am feeling sad"))
        self.assertFalse(self.processor.is_repeat_request("how are you doing"))
        self.assertFalse(self.processor.is_repeat_request("tell me about anxiety"))
        self.assertFalse(self.processor.is_repeat_request("i need help with depression"))
        
        # Longer queries with incidental repeat keywords should not be detected
        self.assertFalse(self.processor.is_repeat_request("i want to understand what depression means"))
        self.assertFalse(self.processor.is_repeat_request("can you say something about anxiety again and again"))
    
    def test_is_repeat_request_edge_cases(self):
        """Test edge cases for repeat detection."""
        # Empty input
        self.assertFalse(self.processor.is_repeat_request(""))
        self.assertFalse(self.processor.is_repeat_request("   "))
        
        # Single characters
        self.assertFalse(self.processor.is_repeat_request("a"))
        self.assertFalse(self.processor.is_repeat_request("?"))
        
        # Mixed case should work
        self.assertTrue(self.processor.is_repeat_request("REPEAT"))
        self.assertTrue(self.processor.is_repeat_request("Say Again"))
        self.assertTrue(self.processor.is_repeat_request("WHAT DID YOU SAY"))
    
    def test_is_repeat_request_normalized_input(self):
        """Test repeat detection with normalized input."""
        # Test with already normalized text (as would be used in practice)
        self.assertTrue(self.processor.is_repeat_request("repeat"))
        self.assertTrue(self.processor.is_repeat_request("say again"))
        self.assertTrue(self.processor.is_repeat_request("what did you say"))
        self.assertTrue(self.processor.is_repeat_request("didnt hear"))
        
        # Test with punctuation and capitalization (should still work)
        self.assertTrue(self.processor.is_repeat_request("Repeat!"))
        self.assertTrue(self.processor.is_repeat_request("Say again?"))
        self.assertTrue(self.processor.is_repeat_request("What did you say???"))
    
    def test_is_repeat_request_context_sensitivity(self):
        """Test that repeat detection is appropriately context-sensitive."""
        # Queries that mention repeat but aren't asking for repeat
        self.assertFalse(self.processor.is_repeat_request("i keep repeating the same mistakes"))
        self.assertFalse(self.processor.is_repeat_request("this happens again and again in my life"))
        self.assertFalse(self.processor.is_repeat_request("what should i do when this pattern repeats"))
        
        # But direct requests should still work
        self.assertTrue(self.processor.is_repeat_request("repeat"))
        self.assertTrue(self.processor.is_repeat_request("what"))
        self.assertTrue(self.processor.is_repeat_request("again"))


if __name__ == '__main__':
    unittest.main()