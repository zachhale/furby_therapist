# Design Document

## Overview

The Furby Therapist CLI is a lightweight, offline therapeutic assistant that combines the whimsical personality of a Furby toy with simple therapeutic responses. The system uses keyword-based matching to select appropriate responses from a pre-defined database, ensuring minimal resource usage and efficient operation.

The design prioritizes simplicity, efficiency, and maintainability while delivering an engaging user experience through Furby-style language patterns and authentic Furbish phrases.

## Architecture

### High-Level Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   CLI Interface │───▶│  Query Processor │───▶│ Response Engine │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │ Keyword Matcher  │    │ Response Database│
                       └──────────────────┘    └─────────────────┘
```

### Core Components

1. **CLI Interface**: Handles user input/output and command-line argument parsing
2. **Query Processor**: Normalizes and prepares user input for keyword matching
3. **Keyword Matcher**: Performs lightweight pattern matching against predefined keywords
4. **Response Engine**: Selects and formats appropriate Furby-style therapeutic responses
5. **Response Database**: Static collection of categorized therapeutic responses

## Components and Interfaces

### CLI Interface (`cli.py`)

**Purpose**: Entry point for user interaction, handles command-line arguments and interactive mode.

**Key Methods**:
- `main()`: Parse arguments and route to appropriate mode
- `interactive_mode()`: Continuous input loop for chat-like interaction
- `single_query_mode(query)`: Process single query and exit
- `format_output(response)`: Apply Furby-style formatting to responses

**Input**: Command-line arguments, user text input
**Output**: Formatted Furby therapeutic responses

### Query Processor (`processor.py`)

**Purpose**: Normalize and prepare user input for keyword matching.

**Key Methods**:
- `normalize_text(input_text)`: Clean and standardize input text
- `extract_keywords(text)`: Identify key emotional and topical words
- `detect_emotion(text)`: Simple emotion detection based on keyword presence

**Processing Steps**:
1. Convert to lowercase
2. Remove punctuation and extra whitespace
3. Extract meaningful keywords
4. Identify emotional indicators

### Keyword Matcher (`matcher.py`)

**Purpose**: Lightweight pattern matching to categorize user queries.

**Key Methods**:
- `match_category(keywords)`: Determine response category based on keywords
- `calculate_confidence(matches)`: Simple scoring for match quality
- `get_fallback_category()`: Default category when no matches found

**Matching Strategy**:
- Simple string containment checks
- Weighted keyword scoring
- Emotion-based categorization
- Fallback to generic supportive responses

### Response Engine (`responses.py`)

**Purpose**: Select and format appropriate therapeutic responses in Furby style.

**Key Methods**:
- `get_response(category, emotion)`: Select response based on category and emotion
- `add_furby_flair(response)`: Add Furby-style language elements
- `maybe_add_furbish(response)`: Randomly include Furbish phrases
- `format_therapeutic_response(base_response)`: Apply therapeutic framing

**Response Selection Logic**:
1. Match category and emotion to response pool
2. Randomly select from appropriate responses
3. Add Furby personality elements
4. Include occasional Furbish phrases with translations

### Response Database (`database.py`)

**Purpose**: Static storage of categorized therapeutic responses.

**Structure**:
```python
RESPONSES = {
    'sadness': {
        'responses': [...],
        'furby_sounds': ['*snuggle*', 'awww', 'me understand'],
        'furbish': [('Kah may-may', 'me love you'), ...]
    },
    'anxiety': {...},
    'general': {...}
}
```

## Data Models

### Response Category Structure

```python
@dataclass
class ResponseCategory:
    name: str
    keywords: List[str]
    responses: List[str]
    furby_sounds: List[str]
    furbish_phrases: List[Tuple[str, str]]  # (furbish, translation)
    weight: float
```

### Query Analysis Result

```python
@dataclass
class QueryAnalysis:
    original_text: str
    normalized_text: str
    keywords: List[str]
    detected_emotion: str
    confidence: float
    category: str
```

### Furby Response

```python
@dataclass
class FurbyResponse:
    base_message: str
    furby_sounds: List[str]
    furbish_phrase: Optional[Tuple[str, str]]
    formatted_output: str
```

## Error Handling

### Input Validation
- Handle empty or whitespace-only input gracefully
- Sanitize input to prevent any potential issues
- Provide friendly error messages in Furby style

### Processing Errors
- Fallback to generic supportive responses if matching fails
- Log errors for debugging while maintaining user experience
- Graceful degradation when response database is incomplete

### Resource Management
- Monitor memory usage and clean up as needed
- Handle file I/O errors when loading response database
- Implement timeout protection for any processing loops

## Testing Strategy

### Unit Testing
- **Query Processor**: Test text normalization and keyword extraction
- **Keyword Matcher**: Verify category matching accuracy and fallback behavior
- **Response Engine**: Test response selection and Furby formatting
- **CLI Interface**: Test argument parsing and output formatting

### Integration Testing
- **End-to-End Flows**: Test complete query-to-response pipeline
- **Error Scenarios**: Verify graceful handling of edge cases
- **Performance**: Ensure reasonable response times

### Manual Testing
- **Therapeutic Quality**: Verify responses feel supportive and appropriate
- **Furby Personality**: Confirm authentic Furby-style language and charm
- **User Experience**: Test interactive mode usability and flow

### Performance Testing
- **Memory Usage**: Verify efficient memory consumption
- **Response Time**: Confirm reasonable response times for typical queries
- **Resource Efficiency**: Test sustained usage without memory leaks

## Implementation Considerations

### Performance Optimization
- Use built-in Python libraries where possible to minimize dependencies
- Implement efficient loading for response database
- Optimize string operations for performance
- Keep data structures simple and memory-efficient

### Furby Authenticity
- Research authentic Furby phrases and speech patterns
- Include genuine Furbish vocabulary with translations
- Maintain whimsical, childlike therapeutic tone
- Balance silly and pensive responses appropriately

### Therapeutic Effectiveness
- Focus on validation, empathy, and gentle encouragement
- Use broad, universally applicable therapeutic principles
- Avoid complex psychological analysis or specific advice
- Maintain appropriate boundaries for a simple assistant

### Extensibility
- Design modular response categories for easy expansion
- Allow for simple addition of new keywords and responses
- Structure code to support future audio integration
- Maintain clean separation between processing and presentation layers