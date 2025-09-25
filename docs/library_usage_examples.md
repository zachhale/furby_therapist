# Furby Therapist Library Usage Examples

This document provides examples of how to use the Furby Therapist library in different scenarios.

## Basic Library Usage

### Simple Single Query Processing

```python
from furby_therapist import process_single_query

# Process a single query without maintaining state
response = process_single_query("I'm feeling sad")
print(response.formatted_output)
```

### Stateful Conversation

```python
from furby_therapist import create_furby_therapist

# Create a therapist that maintains conversation context
therapist = create_furby_therapist(cycling_mode=False, stateful=True)

# Have a conversation
response1 = therapist.process_query("I'm feeling anxious about work")
print(response1.formatted_output)

response2 = therapist.process_query("It's been going on for weeks")
print(response2.formatted_output)

# Clear conversation history if needed
therapist.clear_conversation_history()
```

### Cycling Mode

```python
from furby_therapist import FurbyTherapist

# Create a therapist with cycling-themed responses
cycling_therapist = FurbyTherapist(cycling_mode=True, maintain_session=True)

response = cycling_therapist.process_query("I'm stressed about my performance")
print(response.formatted_output)
# Output will include cycling metaphors and bike culture references
```

## Advanced Usage

### Accessing Response Details

```python
from furby_therapist import FurbyTherapist

therapist = FurbyTherapist()
response = therapist.process_query("I'm happy today!")

# Access different parts of the response
print("Base message:", response.base_message)
print("Furby sounds:", response.furby_sounds)
print("Furbish phrase:", response.furbish_phrase)
print("Clean version:", response.clean_version)
```

### Session Statistics

```python
from furby_therapist import FurbyTherapist

therapist = FurbyTherapist(maintain_session=True)

# Have some conversations
therapist.process_query("I'm feeling down")
therapist.process_query("Work has been stressful")

# Get session statistics
stats = therapist.get_session_stats()
print("Conversation length:", stats['conversation_length'])
print("Recent emotions:", stats['recent_emotions'])
print("Session start:", stats['session_start'])
```

### Repeat Functionality

```python
from furby_therapist import FurbyTherapist

therapist = FurbyTherapist()

# Generate a response
response = therapist.process_query("I need encouragement")
print("Original:", response.formatted_output)

# Get a cleaner repeat version
if therapist.has_cached_response():
    repeat = therapist.get_repeat_response()
    print("Repeat:", repeat.formatted_output)
```

## Integration Examples

### Web Application Integration

```python
from flask import Flask, request, jsonify
from furby_therapist import FurbyTherapist

app = Flask(__name__)

# Create a global therapist instance (in production, use per-session instances)
therapist = FurbyTherapist(cycling_mode=False, maintain_session=False)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    
    try:
        response = therapist.process_query(user_message)
        return jsonify({
            'success': True,
            'response': response.formatted_output,
            'clean_version': response.clean_version
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
```

### Discord Bot Integration

```python
import discord
from discord.ext import commands
from furby_therapist import FurbyTherapist

# Create bot with per-user therapist instances
user_therapists = {}

bot = commands.Bot(command_prefix='!')

@bot.command(name='furby')
async def furby_chat(ctx, *, message):
    user_id = ctx.author.id
    
    # Create or get user's therapist instance
    if user_id not in user_therapists:
        user_therapists[user_id] = FurbyTherapist(maintain_session=True)
    
    therapist = user_therapists[user_id]
    
    try:
        response = therapist.process_query(message)
        await ctx.send(response.formatted_output)
    except Exception as e:
        await ctx.send(f"*sad beep* Furby is having trouble: {e}")

@bot.command(name='furby_bikes')
async def furby_cycling(ctx, *, message):
    # Cycling mode for bike enthusiasts
    cycling_therapist = FurbyTherapist(cycling_mode=True, maintain_session=False)
    
    try:
        response = cycling_therapist.process_query(message)
        await ctx.send(response.formatted_output)
    except Exception as e:
        await ctx.send(f"*sad beep* Furby's chain is stuck: {e}")

# bot.run('YOUR_BOT_TOKEN')
```

### Chatbot with Memory Management

```python
from furby_therapist import FurbyTherapist
import time
from collections import defaultdict

class ManagedFurbyChat:
    def __init__(self, session_timeout=3600):  # 1 hour timeout
        self.sessions = {}
        self.last_activity = defaultdict(float)
        self.session_timeout = session_timeout
    
    def get_therapist(self, session_id, cycling_mode=False):
        """Get or create a therapist for a session."""
        current_time = time.time()
        
        # Clean up old sessions
        self._cleanup_old_sessions(current_time)
        
        # Create new session if needed
        if session_id not in self.sessions:
            self.sessions[session_id] = FurbyTherapist(
                cycling_mode=cycling_mode,
                maintain_session=True
            )
        
        # Update activity time
        self.last_activity[session_id] = current_time
        
        return self.sessions[session_id]
    
    def _cleanup_old_sessions(self, current_time):
        """Remove sessions that have timed out."""
        expired_sessions = [
            sid for sid, last_time in self.last_activity.items()
            if current_time - last_time > self.session_timeout
        ]
        
        for session_id in expired_sessions:
            if session_id in self.sessions:
                self.sessions[session_id].cleanup()
                del self.sessions[session_id]
            del self.last_activity[session_id]
    
    def chat(self, session_id, message, cycling_mode=False):
        """Process a chat message for a session."""
        therapist = self.get_therapist(session_id, cycling_mode)
        return therapist.process_query(message)

# Usage
chat_manager = ManagedFurbyChat()

# Different users can have separate conversations
response1 = chat_manager.chat("user123", "I'm feeling anxious")
response2 = chat_manager.chat("user456", "I love cycling!", cycling_mode=True)
```

## Error Handling

```python
from furby_therapist import FurbyTherapist

therapist = FurbyTherapist()

try:
    response = therapist.process_query("Hello Furby!")
    print(response.formatted_output)
except ValueError as e:
    print(f"Input validation error: {e}")
except RuntimeError as e:
    print(f"Processing error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    # Always cleanup resources
    therapist.cleanup()
```

## Performance Considerations

- Use `maintain_session=False` for stateless applications to save memory
- Implement session cleanup in long-running applications
- Consider using connection pooling for high-traffic scenarios
- The library is designed to be lightweight and efficient for typical usage patterns