"""
Response engine for generating Furby-style therapeutic responses.
"""

import json
import random
from typing import Dict, List, Optional, Tuple
from pathlib import Path

from .models import FurbyResponse, ResponseCategory


class ResponseEngine:
    """Generates Furby-style therapeutic responses based on categorized input."""
    
    def __init__(self, responses_file: Optional[str] = None):
        """Initialize the response engine with response database."""
        if responses_file is None:
            responses_file = Path(__file__).parent / "responses.json"
        
        self.categories = self._load_responses(responses_file)
        self._last_response: Optional[FurbyResponse] = None  # Cache for repeat functionality
        
    def _load_responses(self, responses_file: str) -> Dict[str, ResponseCategory]:
        """Load response categories from JSON file."""
        try:
            with open(responses_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            categories = {}
            for name, category_data in data['categories'].items():
                categories[name] = ResponseCategory(
                    name=name,
                    keywords=category_data['keywords'],
                    responses=category_data['responses'],
                    furby_sounds=category_data['furby_sounds'],
                    furbish_phrases=[(phrase[0], phrase[1]) for phrase in category_data['furbish_phrases']],
                    weight=1.0  # Default weight
                )
            
            return categories
            
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            # Fallback to minimal responses if file loading fails
            return self._create_fallback_responses()
    
    def _create_fallback_responses(self) -> Dict[str, ResponseCategory]:
        """Create minimal fallback responses if JSON loading fails."""
        return {
            'fallback': ResponseCategory(
                name='fallback',
                keywords=[],
                responses=[
                    "Ooh! Furby here to listen! *gentle chirp* Tell me what's on your mind!",
                    "Me think you very brave for sharing! *warm purr* Furby cares about you!"
                ],
                furby_sounds=["*chirp*", "*purr*", "ooh!"],
                furbish_phrases=[("Dah koh-koh", "it's okay"), ("U-nye way-loh", "you matter")],
                weight=1.0
            )
        }
    
    def get_response(self, category: str, emotion: Optional[str] = None) -> FurbyResponse:
        """Generate a Furby-style therapeutic response for the given category and emotion."""
        # Get the appropriate category, fallback if not found
        response_category = self.categories.get(category, self.categories.get('fallback'))
        if not response_category:
            response_category = list(self.categories.values())[0]  # Use first available
        
        # Select base response
        base_message = random.choice(response_category.responses)
        
        # Add Furby flair
        enhanced_message = self.add_furby_flair(base_message, response_category)
        
        # Maybe add Furbish phrase
        furbish_phrase = self.maybe_add_furbish(response_category)
        
        # Format the final response
        formatted_output = self.format_therapeutic_response(
            enhanced_message, 
            furbish_phrase,
            response_category.furby_sounds
        )
        
        # Create clean version for potential repeats
        clean_version = self._create_clean_version(enhanced_message)
        
        # Create response object
        response = FurbyResponse(
            base_message=base_message,
            furby_sounds=response_category.furby_sounds,
            furbish_phrase=furbish_phrase,
            formatted_output=formatted_output,
            clean_version=clean_version
        )
        
        # Cache this response for potential repeat requests
        self._last_response = response
        
        return response
    
    def add_furby_flair(self, response: str, category: ResponseCategory) -> str:
        """Add Furby-style language elements and sound effects to response."""
        # Response already has Furby flair built in from JSON, but we can enhance it
        enhanced = response
        
        # Occasionally add extra Furby sounds at the end (20% chance)
        if random.random() < 0.2:
            extra_sound = random.choice(category.furby_sounds)
            if not enhanced.endswith('!') and not enhanced.endswith('*'):
                enhanced += f" {extra_sound}"
        
        return enhanced
    
    def maybe_add_furbish(self, category: ResponseCategory) -> Optional[Tuple[str, str]]:
        """Randomly include a Furbish phrase with translation (30% chance)."""
        if random.random() < 0.3 and category.furbish_phrases:
            return random.choice(category.furbish_phrases)
        return None
    
    def format_therapeutic_response(
        self, 
        message: str, 
        furbish_phrase: Optional[Tuple[str, str]] = None,
        furby_sounds: Optional[List[str]] = None
    ) -> str:
        """Apply final formatting to create complete therapeutic response."""
        formatted = message
        
        # Add Furbish phrase if present
        if furbish_phrase:
            furbish, translation = furbish_phrase
            formatted += f"\n\n{furbish}! ({translation})"
        
        return formatted
    
    def get_available_categories(self) -> List[str]:
        """Get list of available response categories."""
        return list(self.categories.keys())
    
    def get_category_info(self, category: str) -> Optional[ResponseCategory]:
        """Get information about a specific category."""
        return self.categories.get(category)
    
    def _create_clean_version(self, message: str) -> str:
        """
        Create a clean version of the message without excessive Furby sounds.
        Maintains therapeutic content while being more accessible.
        
        Args:
            message: Enhanced message with Furby flair
            
        Returns:
            Clean version suitable for repeat requests
        """
        import re
        
        # Remove excessive sound effects but keep some personality
        clean = message
        
        # Remove multiple consecutive sound effects like "*chirp* *purr*"
        clean = re.sub(r'\*[^*]+\*\s*\*[^*]+\*', '*gentle sound*', clean)
        
        # Replace specific Furby sounds with gentler alternatives
        sound_replacements = {
            r'\*chirp\*': '',
            r'\*purr\*': '',
            r'\*giggle\*': '',
            r'\*squeak\*': '',
            r'\*beep\*': '',
            r'\*whirr\*': '',
            r'ooh!': '',
            r'eee!': '',
            r'ah!': '',
        }
        
        for pattern, replacement in sound_replacements.items():
            clean = re.sub(pattern, replacement, clean, flags=re.IGNORECASE)
        
        # Clean up extra spaces and punctuation
        clean = re.sub(r'\s+', ' ', clean)
        clean = re.sub(r'\s*,\s*', ', ', clean)
        clean = re.sub(r'\s*!\s*', '! ', clean)
        clean = clean.strip()
        
        # Ensure it ends properly
        if clean and not clean.endswith(('.', '!', '?')):
            clean += '.'
        
        return clean
    
    def get_repeat_response(self) -> Optional[FurbyResponse]:
        """
        Get a repeat of the last response in a cleaner, more accessible format.
        
        Returns:
            FurbyResponse with clean version, or None if no previous response
        """
        if not self._last_response:
            return None
        
        # Create a new response object for the repeat
        repeat_response = FurbyResponse(
            base_message=self._last_response.base_message,
            furby_sounds=self._last_response.furby_sounds,
            furbish_phrase=None,  # No Furbish in repeats
            formatted_output=self._last_response.clean_version or self._last_response.base_message,
            clean_version=self._last_response.clean_version
        )
        
        return repeat_response
    
    def has_cached_response(self) -> bool:
        """Check if there's a cached response available for repeat."""
        return self._last_response is not None
    
    def clear_cache(self) -> None:
        """Clear the cached response."""
        self._last_response = None