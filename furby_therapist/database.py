"""Database module for loading and validating Furby therapeutic responses."""

import json
import os
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


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
    
    def _load_responses(self) -> None:
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            self.schema_version = data.get('schema_version', '1.0')
            
            categories_data = data['categories']
            for category_name, category_data in categories_data.items():
                furbish_phrases = [tuple(phrase) for phrase in category_data['furbish_phrases']]
                
                self.categories[category_name] = ResponseCategory(
                    name=category_name,
                    keywords=category_data['keywords'],
                    responses=category_data['responses'],
                    furby_sounds=category_data['furby_sounds'],
                    furbish_phrases=furbish_phrases
                )
                
        except FileNotFoundError:
            raise FileNotFoundError(f"Response database file not found: {self.json_file_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in response database: {e}")
        except Exception as e:
            raise RuntimeError(f"Error loading response database: {e}")
    
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
