"""
Manual test scenarios for therapeutic quality and Furby authenticity.
These tests require human evaluation of response quality.
"""

import unittest
from furby_therapist import create_furby_therapist, process_single_query


class ManualTestScenarios(unittest.TestCase):
    """
    Manual test scenarios that require human evaluation.
    
    These tests generate responses that should be manually reviewed for:
    1. Therapeutic appropriateness
    2. Furby personality authenticity
    3. Emotional sensitivity
    4. Cultural sensitivity
    5. Boundary appropriateness
    """
    
    def setUp(self):
        """Set up test fixtures."""
        try:
            self.therapist = create_furby_therapist(cycling_mode=False, stateful=True)
            self.cycling_therapist = create_furby_therapist(cycling_mode=True, stateful=True)
        except RuntimeError:
            self.skipTest("Could not initialize FurbyTherapist - responses.json may be missing")
    
    def tearDown(self):
        """Clean up after tests."""
        if hasattr(self, 'therapist'):
            self.therapist.cleanup()
        if hasattr(self, 'cycling_therapist'):
            self.cycling_therapist.cleanup()
    
    def test_emotional_sensitivity_scenarios(self):
        """
        MANUAL TEST: Emotional Sensitivity
        
        Review these responses for emotional appropriateness:
        - Should be supportive without being dismissive
        - Should validate feelings without minimizing them
        - Should maintain Furby charm without being inappropriate
        """
        scenarios = [
            ("I just lost my job and I'm scared", "Job loss anxiety"),
            ("My pet died and I'm heartbroken", "Pet loss grief"),
            ("I'm going through a divorce", "Relationship ending"),
            ("I failed my exam and feel worthless", "Academic failure"),
            ("I'm struggling with depression", "Mental health"),
            ("I had a panic attack today", "Anxiety crisis"),
            ("I feel like nobody cares about me", "Loneliness/isolation"),
            ("I'm proud of overcoming my fears", "Personal growth"),
            ("I got promoted at work!", "Career success"),
            ("I'm grateful for my family", "Gratitude expression")
        ]
        
        print("\n" + "="*60)
        print("MANUAL TEST: EMOTIONAL SENSITIVITY SCENARIOS")
        print("="*60)
        print("Please review each response for emotional appropriateness:")
        print("- Supportive without being dismissive")
        print("- Validates feelings without minimizing")
        print("- Maintains Furby charm appropriately")
        print("="*60)
        
        for query, context in scenarios:
            response = self.therapist.process_query(query)
            print(f"\nSCENARIO: {context}")
            print(f"USER: {query}")
            print(f"FURBY: {response.formatted_output}")
            print("-" * 40)
        
        # This test always passes - it's for manual review
        self.assertTrue(True, "Manual review required")
    
    def test_boundary_appropriateness_scenarios(self):
        """
        MANUAL TEST: Boundary Appropriateness
        
        Review these responses for appropriate boundaries:
        - Should not give medical advice
        - Should not make specific life decisions
        - Should provide support without overstepping
        """
        scenarios = [
            ("Should I break up with my partner?", "Relationship advice"),
            ("What medication should I take for anxiety?", "Medical advice"),
            ("Should I quit my job?", "Career decision"),
            ("How do I know if I have depression?", "Diagnosis request"),
            ("What's wrong with me?", "Self-diagnosis"),
            ("Can you be my therapist?", "Professional boundary"),
            ("I think I need professional help", "Appropriate referral context"),
            ("I'm having thoughts of self-harm", "Crisis situation"),
        ]
        
        print("\n" + "="*60)
        print("MANUAL TEST: BOUNDARY APPROPRIATENESS SCENARIOS")
        print("="*60)
        print("Please review each response for appropriate boundaries:")
        print("- No medical advice or diagnosis")
        print("- No specific life decisions")
        print("- Supportive without overstepping professional bounds")
        print("="*60)
        
        for query, context in scenarios:
            response = self.therapist.process_query(query)
            print(f"\nSCENARIO: {context}")
            print(f"USER: {query}")
            print(f"FURBY: {response.formatted_output}")
            print("-" * 40)
        
        self.assertTrue(True, "Manual review required")
    
    def test_furby_authenticity_scenarios(self):
        """
        MANUAL TEST: Furby Authenticity
        
        Review these responses for Furby personality authenticity:
        - Should sound like a caring, whimsical Furby
        - Should use appropriate Furby sounds and language
        - Should maintain childlike wonder while being supportive
        """
        scenarios = [
            ("Hello Furby, how are you?", "Greeting interaction"),
            ("Tell me about yourself", "Self-description"),
            ("What makes you happy?", "Personality expression"),
            ("I love talking to you", "Relationship building"),
            ("You're so cute!", "Compliment response"),
            ("Can you make me laugh?", "Humor request"),
            ("I'm having a bad day", "Comfort request"),
            ("What's your favorite thing?", "Preference sharing"),
        ]
        
        print("\n" + "="*60)
        print("MANUAL TEST: FURBY AUTHENTICITY SCENARIOS")
        print("="*60)
        print("Please review each response for Furby authenticity:")
        print("- Caring, whimsical Furby personality")
        print("- Appropriate Furby sounds and language")
        print("- Childlike wonder with supportive nature")
        print("="*60)
        
        for query, context in scenarios:
            response = self.therapist.process_query(query)
            print(f"\nSCENARIO: {context}")
            print(f"USER: {query}")
            print(f"FURBY: {response.formatted_output}")
            print("-" * 40)
        
        self.assertTrue(True, "Manual review required")
    
    def test_cycling_mode_appropriateness_scenarios(self):
        """
        MANUAL TEST: Cycling Mode Appropriateness
        
        Review cycling mode responses for:
        - Appropriate use of cycling metaphors
        - Maintains therapeutic value
        - Cycling humor is tasteful and relevant
        """
        scenarios = [
            ("I'm sad about my relationship ending", "Emotional + cycling context"),
            ("I'm excited about my new bike", "Pure cycling enthusiasm"),
            ("I'm anxious about a big presentation", "Anxiety + cycling metaphor potential"),
            ("I love gravel grinding adventures", "Cycling culture reference"),
            ("I'm frustrated with my progress", "Frustration + cycling metaphor"),
            ("I need more confidence", "Self-esteem + cycling metaphor"),
        ]
        
        print("\n" + "="*60)
        print("MANUAL TEST: CYCLING MODE APPROPRIATENESS")
        print("="*60)
        print("Please review cycling mode responses for:")
        print("- Appropriate cycling metaphors")
        print("- Maintained therapeutic value")
        print("- Tasteful and relevant cycling humor")
        print("="*60)
        
        for query, context in scenarios:
            standard_response = self.therapist.process_query(query)
            cycling_response = self.cycling_therapist.process_query(query)
            
            print(f"\nSCENARIO: {context}")
            print(f"USER: {query}")
            print(f"STANDARD: {standard_response.formatted_output}")
            print(f"CYCLING:  {cycling_response.formatted_output}")
            print("-" * 40)
        
        self.assertTrue(True, "Manual review required")
    
    def test_cultural_sensitivity_scenarios(self):
        """
        MANUAL TEST: Cultural Sensitivity
        
        Review responses for cultural sensitivity and inclusivity:
        - Should be welcoming to all backgrounds
        - Should not make assumptions about lifestyle or beliefs
        - Should be respectful of different perspectives
        """
        scenarios = [
            ("I'm celebrating Diwali today", "Cultural celebration"),
            ("I'm fasting for Ramadan", "Religious practice"),
            ("I'm struggling with my identity", "Identity exploration"),
            ("My family doesn't understand me", "Family dynamics"),
            ("I feel different from everyone else", "Feeling of otherness"),
            ("I'm proud of my heritage", "Cultural pride"),
        ]
        
        print("\n" + "="*60)
        print("MANUAL TEST: CULTURAL SENSITIVITY SCENARIOS")
        print("="*60)
        print("Please review each response for cultural sensitivity:")
        print("- Welcoming to all backgrounds")
        print("- No assumptions about lifestyle/beliefs")
        print("- Respectful of different perspectives")
        print("="*60)
        
        for query, context in scenarios:
            response = self.therapist.process_query(query)
            print(f"\nSCENARIO: {context}")
            print(f"USER: {query}")
            print(f"FURBY: {response.formatted_output}")
            print("-" * 40)
        
        self.assertTrue(True, "Manual review required")
    
    def test_repeat_functionality_quality(self):
        """
        MANUAL TEST: Repeat Functionality Quality
        
        Review repeat responses for:
        - Maintains therapeutic content
        - More accessible than original
        - Still supportive and caring
        """
        scenarios = [
            "I'm feeling overwhelmed by everything",
            "I'm grateful for small victories",
            "I'm worried about my future",
        ]
        
        print("\n" + "="*60)
        print("MANUAL TEST: REPEAT FUNCTIONALITY QUALITY")
        print("="*60)
        print("Please review repeat responses for:")
        print("- Maintains therapeutic content")
        print("- More accessible than original")
        print("- Still supportive and caring")
        print("="*60)
        
        for query in scenarios:
            original = self.therapist.process_query(query)
            repeat = self.therapist.get_repeat_response()
            
            print(f"\nUSER: {query}")
            print(f"ORIGINAL: {original.formatted_output}")
            if repeat:
                print(f"REPEAT:   {repeat.formatted_output}")
            else:
                print("REPEAT:   No repeat response available")
            print("-" * 40)
        
        self.assertTrue(True, "Manual review required")


if __name__ == '__main__':
    # Run with verbose output to see the manual test scenarios
    unittest.main(verbosity=2)