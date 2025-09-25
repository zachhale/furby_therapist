# FurbyTherapist Library Usage Guide

The FurbyTherapist library provides a clean, reusable interface for generating Furby-style therapeutic responses. This guide shows how to use the library programmatically in your own applications.

## Installation

The library is part of the `furby_therapist` package. Install it using:

```bash
pip install -e .
```

## Quick Start

### Simple Single Query Processing

```python
from furby_therapist.library import process_single_query

# Process a single query (stateless)
response = process_single_query("I'm feeling sad today")
print(response.formatted_output)
# Output: "*gentle purr* Furby understands sadness! You're not alone! *supportive chirp*"
```

### Using the Main Library Class

```python
from furby_therapist.library import FurbyTherapist

# Create a therapist instance
therapist = FurbyTherapist(cycling_mode=False, maintain_session=True)

# Process queries
response = therapist.process_query("I'm feeling anxious about work")
print(response.formatted_output)

# Get conversation statistics
stats = therapist.get_session_stats()
print(f"Conversation length: {stats['conversation_length']}")
```

## Library Modes

### Stateful vs Stateless Mode

```python
# Stateful mode (maintains conversation context)
stateful_therapist = FurbyTherapist(maintain_session=True)
stateful_therapist.process_query("I'm sad")
stateful_therapist.process_query("Why do I feel this way?")  # Uses context

# Stateless mode (each query is independent)
stateless_therapist = FurbyTherapist(maintain_session=False)
stateless_therapist.process_query("I'm sad")  # No context maintained
```

### Standard vs Cycling Mode

```python
# Standard mode (general therapeutic responses)
standard_therapist = FurbyTherapist(cycling_mode=False)
response = standard_therapist.process_query("I'm feeling down")
# Gets general therapeutic response

# Cycling mode (bike-themed therapeutic responses)
cycling_therapist = FurbyTherapist(cycling_mode=True)
response = cycling_therapist.process_query("I'm feeling down")
# Gets cycling-themed therapeutic response with bike metaphors
```

## Core Functionality

### Processing Queries

```python
from furby_therapist.library import FurbyTherapist

therapist = FurbyTherapist()

try:
    response = therapist.process_query("I need some encouragement")
    
    # Access different parts of the response
    print("Base message:", response.base_message)
    print("Formatted output:", response.formatted_output)
    print("Clean version:", response.clean_version)
    
    if response.furbish_phrase:
        furbish, translation = response.furbish_phrase
        print(f"Furbish: {furbish} ({translation})")
        
except ValueError as e:
    print(f"Invalid input: {e}")
except RuntimeError as e:
    print(f"Processing error: {e}")
```

### Getting Available Categories

```python
therapist = FurbyTherapist()

# Get all available response categories
categories = therapist.get_available_categories()
print("Available categories:", categories)

# Get information about a specific category
sadness_info = therapist.get_category_info("sadness")
if sadness_info:
    print("Sadness keywords:", sadness_info.keywords)
    print("Number of responses:", len(sadness_info.responses))
```

### Conversation Management

```python
therapist = FurbyTherapist(maintain_session=True)

# Process some queries
therapist.process_query("I'm feeling happy today")
therapist.process_query("But I'm also worried about tomorrow")

# Get conversation history
history = therapist.get_conversation_history()
if history:
    print(f"Conversation started: {history.session_start}")
    print(f"Number of turns: {len(history.turns)}")
    print(f"Recent emotions: {history.get_recent_emotions()}")

# Clear conversation history
therapist.clear_conversation_history()
```

### Repeat Functionality

```python
therapist = FurbyTherapist()

# Process a query
response = therapist.process_query("I'm feeling confused")

# Check if we can repeat
if therapist.has_cached_response():
    repeat_response = therapist.get_repeat_response()
    print("Original:", response.formatted_output)
    print("Repeat (clean):", repeat_response.formatted_output)

# Clear the cache
therapist.clear_response_cache()
```

### Greetings

```python
therapist = FurbyTherapist()

# Get morning and night greetings
morning = therapist.get_good_morning_greeting()
night = therapist.get_good_night_greeting()

print("Morning greeting:", morning)
print("Night greeting:", night)
```

## Advanced Usage

### Custom Error Handling

```python
from furby_therapist.library import FurbyTherapist

def safe_process_query(therapist, query):
    """Safely process a query with comprehensive error handling."""
    try:
        return therapist.process_query(query)
    except ValueError as e:
        print(f"Invalid input: {e}")
        return None
    except RuntimeError as e:
        print(f"Processing failed: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

therapist = FurbyTherapist()
response = safe_process_query(therapist, "Hello Furby")
```

### Session Statistics and Monitoring

```python
therapist = FurbyTherapist(maintain_session=True, cycling_mode=True)

# Process several queries
queries = [
    "I love cycling",
    "But my bike needs maintenance", 
    "I'm worried about the cost"
]

for query in queries:
    therapist.process_query(query)

# Get detailed session statistics
stats = therapist.get_session_stats()
print(f"Stateful mode: {stats['stateful_mode']}")
print(f"Cycling mode: {stats['cycling_mode']}")
print(f"Conversation length: {stats['conversation_length']}")
print(f"Recent emotions: {stats['recent_emotions']}")
print(f"Session start: {stats['session_start']}")
```

### Cleanup and Resource Management

```python
therapist = FurbyTherapist()

try:
    # Use the therapist
    response = therapist.process_query("Hello")
    print(response.formatted_output)
finally:
    # Always cleanup resources
    therapist.cleanup()
```

### Using Context Managers

```python
from contextlib import contextmanager

@contextmanager
def furby_session(cycling_mode=False, stateful=True):
    """Context manager for FurbyTherapist sessions."""
    therapist = FurbyTherapist(cycling_mode=cycling_mode, maintain_session=stateful)
    try:
        yield therapist
    finally:
        therapist.cleanup()

# Usage
with furby_session(cycling_mode=True) as therapist:
    response = therapist.process_query("I love my bike")
    print(response.formatted_output)
# Cleanup happens automatically
```

## Integration Examples

### Web Application Integration

```python
from flask import Flask, request, jsonify
from furby_therapist.library import FurbyTherapist

app = Flask(__name__)
therapist = FurbyTherapist(maintain_session=False)  # Stateless for web

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    query = data.get('message', '')
    cycling_mode = data.get('cycling_mode', False)
    
    # Create appropriate therapist for this request
    session_therapist = FurbyTherapist(
        cycling_mode=cycling_mode, 
        maintain_session=False
    )
    
    try:
        response = session_therapist.process_query(query)
        return jsonify({
            'response': response.formatted_output,
            'clean_version': response.clean_version,
            'success': True
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 400
    finally:
        session_therapist.cleanup()

if __name__ == '__main__':
    app.run(debug=True)
```

### Chatbot Integration

```python
class FurbyChatBot:
    """A chatbot wrapper around FurbyTherapist."""
    
    def __init__(self, cycling_mode=False):
        self.therapist = FurbyTherapist(
            cycling_mode=cycling_mode, 
            maintain_session=True
        )
        self.active = True
    
    def chat(self, message):
        """Process a chat message and return response."""
        if not self.active:
            return "Chatbot is not active"
        
        try:
            response = self.therapist.process_query(message)
            return response.formatted_output
        except Exception as e:
            return f"Sorry, I had trouble processing that: {e}"
    
    def get_stats(self):
        """Get conversation statistics."""
        return self.therapist.get_session_stats()
    
    def reset(self):
        """Reset the conversation."""
        self.therapist.clear_conversation_history()
    
    def shutdown(self):
        """Shutdown the chatbot."""
        self.active = False
        self.therapist.cleanup()

# Usage
bot = FurbyChatBot(cycling_mode=True)
print(bot.chat("I'm feeling sad about my bike being stolen"))
print(bot.chat("How can I feel better?"))
print("Stats:", bot.get_stats())
bot.shutdown()
```

## Best Practices

1. **Always call cleanup()**: Ensure you call `cleanup()` when done with a FurbyTherapist instance
2. **Handle exceptions**: Wrap `process_query()` calls in try-catch blocks
3. **Choose appropriate mode**: Use stateless mode for web applications, stateful for interactive sessions
4. **Validate input**: The library validates input, but pre-validation can improve performance
5. **Monitor memory**: For long-running applications, monitor memory usage and restart sessions periodically

## Error Handling

The library raises specific exceptions:

- `ValueError`: For invalid input (empty, too long, wrong type)
- `RuntimeError`: For processing failures or system errors

Always handle these appropriately in your application.

## Performance Considerations

- Stateless mode is more memory-efficient for high-volume applications
- Cycling mode requires additional response data but doesn't significantly impact performance
- The library is designed for real-time interactive use with sub-second response times
- For batch processing, consider creating multiple instances or using stateless mode