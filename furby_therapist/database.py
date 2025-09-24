"""Database module for loading and validating Furby therapeutic responses."""

import json
import os
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

from .error_handler import safe_file_operation


@dataclass
class ResponseCategory:
    name: str
    keywords: List[str]
    responses: List[str]
    furby_sounds: List[str]
    furbish_phrases: List[Tuple[str, str]]


class ResponseDatabase:
    def __init__(self, json_file_path: str = None):
        if json_file_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            json_file_path = os.path.join(current_dir, 'responses.json')
        
        self.json_file_path = json_file_path
        self.categories: Dict[str, ResponseCategory] = {}
        self.schema_version: str = ""
        self._load_responses()
    
    @safe_file_operation("response database loading")
    def _load_responses(self) -> None:
        """Load and validate response database with comprehensive error handling."""
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            # Validate basic structure
            if not isinstance(data, dict):
                raise ValueError("Response database must be a JSON object")
            
            if 'categories' not in data:
                raise ValueError("Response database missing 'categories' key")
            
            self.schema_version = data.get('schema_version', '1.0')
            categories_data = data['categories']
            
            if not isinstance(categories_data, dict):
                raise ValueError("Categories must be a JSON object")
            
            # Validate and load each category
            for category_name, category_data in categories_data.items():
                self._validate_category_data(category_name, category_data)
                
                furbish_phrases = [tuple(phrase) for phrase in category_data['furbish_phrases']]
                
                self.categories[category_name] = ResponseCategory(
                    name=category_name,
                    keywords=category_data['keywords'],
                    responses=category_data['responses'],
                    furby_sounds=category_data['furby_sounds'],
                    furbish_phrases=furbish_phrases
                )
            
            # Ensure fallback category exists
            if 'fallback' not in self.categories:
                raise ValueError("Response database must include a 'fallback' category")
                
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in response database: {e}")
        except (KeyError, TypeError) as e:
            raise ValueError(f"Invalid response database structure: {e}")
        except Exception as e:
            raise RuntimeError(f"Error loading response database: {e}")
    
    def _validate_category_data(self, category_name: str, category_data: dict) -> None:
        """Validate individual category data structure."""
        required_fields = ['keywords', 'responses', 'furby_sounds', 'furbish_phrases']
        
        for field in required_fields:
            if field not in category_data:
                raise ValueError(f"Category '{category_name}' missing required field: {field}")
            
            if not isinstance(category_data[field], list):
                raise ValueError(f"Category '{category_name}' field '{field}' must be a list")
        
        # Validate responses are not empty
        if not category_data['responses']:
            raise ValueError(f"Category '{category_name}' must have at least one response")
        
        # Validate furbish phrases structure
        for i, phrase in enumerate(category_data['furbish_phrases']):
            if not isinstance(phrase, list) or len(phrase) != 2:
                raise ValueError(f"Category '{category_name}' furbish phrase {i} must be [furbish, translation]")
            
            if not all(isinstance(item, str) for item in phrase):
                raise ValueError(f"Category '{category_name}' furbish phrase {i} must contain strings")
    
    def get_category(self, category_name: str) -> Optional[ResponseCategory]:
        return self.categories.get(category_name)
    
    def get_all_categories(self) -> Dict[str, ResponseCategory]:
        return self.categories.copy()
    
    def get_category_names(self) -> List[str]:
        return list(self.categories.keys())
    
    def get_fallback_category(self) -> ResponseCategory:
        fallback = self.get_category('fallback')
        if fallback is None:
            raise RuntimeError("Fallback category not found in response database")
        return fallback


def load_response_database(json_file_path: str = None) -> ResponseDatabase:
    return ResponseDatabase(json_file_path)


if __name__ == "__main__":
    try:
        db = load_response_database()
        print(f"Loaded response database (schema version: {db.schema_version})")
        print(f"Categories: {', '.join(db.get_category_names())}")
        
        sadness_category = db.get_category('sadness')
        if sadness_category:
            print(f"Sample category 'sadness':")
            print(f"  Keywords: {sadness_category.keywords[:5]}...")
            print(f"  Responses: {len(sadness_category.responses)} total")
            print(f"  Furby sounds: {sadness_category.furby_sounds}")
            print(f"  Furbish phrases: {len(sadness_category.furbish_phrases)} total")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
