"""
Tests for data models.
"""

import unittest
from furby_therapist.models import QueryAnalysis, ResponseCategory, FurbyResponse


class TestModels(unittest.TestCase):
    """Test cases for data models."""
    
    def test_query_analysis_creation(self):
        """Test QueryAnalysis dataclass creation."""
        analysis = QueryAnalysis(
            original_text="I feel sad",
            normalized_text="i feel sad",
            keywords=["feel", "sad"],
            detected_emotion="sadness",
            confidence=0.8,
            category="sadness"
        )
        
        self.assertEqual(analysis.original_text, "I feel sad")
        self.assertEqual(analysis.normalized_text, "i feel sad")
        self.assertEqual(analysis.keywords, ["feel", "sad"])
        self.assertEqual(analysis.detected_emotion, "sadness")
        self.assertEqual(analysis.confidence, 0.8)
        self.assertEqual(analysis.category, "sadness")
    
    def test_response_category_creation(self):
        """Test ResponseCategory dataclass creation."""
        category = ResponseCategory(
            name="sadness",
            keywords=["sad", "down", "blue"],
            responses=["Me understand", "Furby here for you"],
            furby_sounds=["*snuggle*", "awww"],
            furbish_phrases=[("Kah may-may", "me love you")],
            weight=1.0
        )
        
        self.assertEqual(category.name, "sadness")
        self.assertEqual(len(category.keywords), 3)
        self.assertEqual(len(category.responses), 2)
        self.assertEqual(len(category.furby_sounds), 2)
        self.assertEqual(len(category.furbish_phrases), 1)
        self.assertEqual(category.weight, 1.0)
    
    def test_furby_response_creation(self):
        """Test FurbyResponse dataclass creation."""
        response = FurbyResponse(
            base_message="Me understand how you feel",
            furby_sounds=["*snuggle*"],
            furbish_phrase=("Kah may-may", "me love you"),
            formatted_output="*snuggle* Me understand how you feel. Kah may-may (me love you)!"
        )
        
        self.assertEqual(response.base_message, "Me understand how you feel")
        self.assertEqual(response.furby_sounds, ["*snuggle*"])
        self.assertEqual(response.furbish_phrase, ("Kah may-may", "me love you"))
        self.assertIn("snuggle", response.formatted_output)


if __name__ == "__main__":
    unittest.main()