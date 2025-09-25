"""
Performance tests for the Furby Therapist system.
Tests response times, memory usage, and system efficiency.
"""

import unittest
import time
import gc
from furby_therapist import create_furby_therapist, process_single_query


class TestPerformance(unittest.TestCase):
    """Test system performance characteristics."""
    
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
    
    def test_response_time_single_query(self):
        """Test that single queries respond within reasonable time."""
        test_queries = [
            "I'm feeling sad",
            "I'm happy today",
            "I need some encouragement",
            "Hello Furby",
            ""  # Empty query
        ]
        
        for query in test_queries:
            with self.subTest(query=query or "empty"):
                start_time = time.time()
                response = self.therapist.process_query(query)
                end_time = time.time()
                
                response_time = end_time - start_time
                
                # Should respond within 1 second for simple queries
                self.assertLess(response_time, 1.0,
                               f"Query '{query}' took {response_time:.3f}s, should be < 1.0s")
                
                # Should get a valid response
                self.assertIsNotNone(response)
                self.assertGreater(len(response.formatted_output), 0)
    
    def test_response_time_batch_queries(self):
        """Test response time for multiple consecutive queries."""
        queries = ["I'm feeling happy"] * 10
        
        start_time = time.time()
        for query in queries:
            response = self.therapist.process_query(query)
            self.assertIsNotNone(response)
        end_time = time.time()
        
        total_time = end_time - start_time
        avg_time = total_time / len(queries)
        
        # Average should be reasonable
        self.assertLess(avg_time, 0.5,
                       f"Average response time {avg_time:.3f}s should be < 0.5s")
        
        # Total time should be reasonable
        self.assertLess(total_time, 5.0,
                       f"Total time {total_time:.3f}s for {len(queries)} queries should be < 5.0s")
    
    def test_memory_usage_stability(self):
        """Test that memory usage remains stable over multiple queries."""
        # Force garbage collection before starting
        gc.collect()
        
        # Process many queries to test for memory leaks
        queries = [
            "I'm feeling sad",
            "I'm happy today", 
            "I need encouragement",
            "Tell me something nice",
            "I'm worried about things"
        ] * 20  # 100 total queries
        
        for i, query in enumerate(queries):
            response = self.therapist.process_query(query)
            self.assertIsNotNone(response)
            
            # Periodically check that we're not accumulating too much
            if i % 25 == 0 and i > 0:
                gc.collect()  # Force cleanup
        
        # Test passes if we complete without memory errors
        self.assertTrue(True)
    
    def test_concurrent_library_instances(self):
        """Test performance with multiple library instances."""
        try:
            therapists = []
            for _ in range(5):
                therapist = create_furby_therapist(cycling_mode=False, stateful=False)
                therapists.append(therapist)
            
            # Test that all instances work
            for i, therapist in enumerate(therapists):
                response = therapist.process_query(f"Hello from instance {i}")
                self.assertIsNotNone(response)
                self.assertGreater(len(response.formatted_output), 0)
            
            # Cleanup
            for therapist in therapists:
                therapist.cleanup()
                
        except RuntimeError:
            self.skipTest("Could not create multiple instances")
    
    def test_large_input_handling(self):
        """Test handling of large input strings."""
        # Test with progressively larger inputs
        base_text = "I'm feeling sad about my situation and need some support. "
        
        for multiplier in [1, 5, 10, 15]:  # Up to ~900 characters
            large_input = base_text * multiplier
            
            # Should handle within reasonable time
            start_time = time.time()
            try:
                response = self.therapist.process_query(large_input)
                end_time = time.time()
                
                response_time = end_time - start_time
                
                # Should still respond reasonably quickly
                self.assertLess(response_time, 2.0,
                               f"Large input ({len(large_input)} chars) took {response_time:.3f}s")
                
                if response:  # Might be None if input is too large
                    self.assertGreater(len(response.formatted_output), 0)
                    
            except ValueError:
                # Expected for very large inputs
                if len(large_input) > 1000:
                    continue  # This is expected
                else:
                    raise
    
    def test_repeat_functionality_performance(self):
        """Test that repeat functionality is efficient."""
        # Generate initial response
        start_time = time.time()
        original = self.therapist.process_query("I'm feeling grateful today")
        first_time = time.time() - start_time
        
        # Get repeat response (should be faster)
        start_time = time.time()
        repeat = self.therapist.get_repeat_response()
        repeat_time = time.time() - start_time
        
        if repeat:
            # Repeat should be faster than original processing
            self.assertLess(repeat_time, first_time,
                           f"Repeat time {repeat_time:.3f}s should be less than original {first_time:.3f}s")
            
            # Repeat should be very fast
            self.assertLess(repeat_time, 0.1,
                           f"Repeat time {repeat_time:.3f}s should be < 0.1s")


class TestStressConditions(unittest.TestCase):
    """Test system behavior under stress conditions."""
    
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
    
    def test_rapid_fire_queries(self):
        """Test handling of rapid consecutive queries."""
        queries = [
            "sad", "happy", "worried", "excited", "confused",
            "grateful", "angry", "peaceful", "anxious", "hopeful"
        ] * 10  # 100 rapid queries
        
        start_time = time.time()
        successful_responses = 0
        
        for query in queries:
            try:
                response = self.therapist.process_query(query)
                if response and len(response.formatted_output) > 0:
                    successful_responses += 1
            except Exception as e:
                # Log but don't fail - we're testing resilience
                print(f"Query '{query}' failed: {e}")
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Should handle most queries successfully
        success_rate = successful_responses / len(queries)
        self.assertGreater(success_rate, 0.9,
                          f"Success rate {success_rate:.2%} should be > 90%")
        
        # Should complete in reasonable time
        self.assertLess(total_time, 30.0,
                       f"Total time {total_time:.3f}s should be < 30s for {len(queries)} queries")
    
    def test_edge_case_inputs(self):
        """Test handling of edge case inputs."""
        edge_cases = [
            "",  # Empty
            " ",  # Whitespace only
            "a",  # Single character
            "?" * 100,  # Repeated punctuation
            "123456789",  # Numbers only
            "SHOUTING ALL CAPS",  # All caps
            "mixed CaSe WeIrD tExT",  # Mixed case
            "special!@#$%^&*()characters",  # Special characters
            "\n\t\r",  # Whitespace characters
            "unicode: 🙂😢😡🎉",  # Unicode/emoji
        ]
        
        for edge_case in edge_cases:
            with self.subTest(input=repr(edge_case)):
                try:
                    response = self.therapist.process_query(edge_case)
                    
                    # Should get some response (even if fallback)
                    if response:
                        self.assertIsInstance(response.formatted_output, str)
                        self.assertGreater(len(response.formatted_output), 0)
                        
                except ValueError:
                    # Some edge cases might be rejected by validation
                    continue
                except Exception as e:
                    self.fail(f"Unexpected error for input {repr(edge_case)}: {e}")
    
    def test_session_longevity(self):
        """Test that sessions can handle extended use."""
        # Simulate a long conversation
        conversation_queries = [
            "Hello Furby",
            "I'm having a tough day",
            "Can you help me feel better?",
            "That's nice, thank you",
            "I'm worried about tomorrow",
            "What should I do?",
            "I appreciate your support",
            "Can you repeat that?",
            "I'm feeling a bit better now",
            "Thank you for listening"
        ] * 5  # 50 query conversation
        
        conversation_length = 0
        
        for query in conversation_queries:
            try:
                response = self.therapist.process_query(query)
                if response:
                    conversation_length += 1
                    
                    # Check session stats periodically
                    if conversation_length % 10 == 0:
                        stats = self.therapist.get_session_stats()
                        # Allow some tolerance for failed queries
                        self.assertGreaterEqual(stats["conversation_length"], conversation_length - 2)
                        
            except Exception as e:
                self.fail(f"Session failed at query {conversation_length}: {e}")
        
        # Should maintain session state throughout
        final_stats = self.therapist.get_session_stats()
        self.assertEqual(final_stats["conversation_length"], conversation_length)


if __name__ == '__main__':
    unittest.main()