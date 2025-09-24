#!/usr/bin/env python3
"""
Interactive test script for the keyword matcher functionality.
"""

from furby_therapist.matcher import KeywordMatcher
from furby_therapist.database import load_response_database
from furby_therapist.processor import QueryProcessor
import sys

def main():
    """Run interactive test of the keyword matcher."""
    try:
        # Load the response database
        print("🔮 Loading Furby response database...")
        db = load_response_database()
        
        # Initialize components
        matcher = KeywordMatcher(db)
        processor = QueryProcessor()
        
        print("✨ Furby Keyword Matcher Test - Interactive Mode")
        print("=" * 50)
        print("Enter queries to test the keyword matching system.")
        print("Type 'quit', 'exit', or press Ctrl+C to exit.")
        print("=" * 50)
        
        while True:
            try:
                # Get user input
                user_input = input("\n💭 Enter your query: ").strip()
                
                # Check for exit commands
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n👋 Goodbye! Thanks for testing the Furby matcher!")
                    break
                
                if not user_input:
                    print("⚠️  Please enter a query to test.")
                    continue
                
                # Process the query
                print(f"\n🔍 Processing: '{user_input}'")
                
                # Normalize and extract keywords
                normalized = processor.normalize_text(user_input)
                keywords = processor.extract_keywords(normalized)
                
                print(f"📝 Normalized: '{normalized}'")
                print(f"🔑 Keywords: {keywords}")
                
                # Match category
                category, confidence = matcher.match_category(keywords)
                
                # Perform complete analysis
                analysis = matcher.analyze_query(normalized, keywords)
                
                # Display results
                print(f"\n📊 Analysis Results:")
                print(f"   Category: {analysis.category}")
                print(f"   Emotion: {analysis.detected_emotion}")
                print(f"   Confidence: {analysis.confidence:.2f}")
                
                # Show sample response from the category
                category_data = db.get_category(analysis.category)
                if category_data and category_data.responses:
                    sample_response = category_data.responses[0]
                    print(f"\n🎭 Sample Furby Response:")
                    print(f"   \"{sample_response}\"")
                
                print("-" * 50)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Thanks for testing the Furby matcher!")
                break
            except Exception as e:
                print(f"\n❌ Error processing query: {e}")
                continue
                
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()