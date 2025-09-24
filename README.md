# Furby Therapist CLI

A therapeutic assistant that combines the whimsical personality of a Furby toy with simple therapeutic responses. Features a unique cycling culture twist with deep knowledge of bike geometry, alt cycling communities, and cycling-themed therapeutic metaphors. Designed to run efficiently with minimal resource usage.

## Features

- Offline therapeutic responses in Furby-style language
- Interactive CLI interface with continuous conversation mode
- Authentic Furbish phrases with English translations
- **Cycling Culture Integration**: Deep knowledge of bike geometry, alt cycling communities, and cycling magazines
- **Therapeutic Cycling Metaphors**: Uses bike mechanics and cycling experiences as therapeutic analogies
- **Bike Geometry Expertise**: Understands reach/stack ratios, chainstay length, head angles, and wheelbase effects
- Lightweight design with minimal resource usage
- Simple keyword-based response matching

## Installation

```bash
pip install -e .
```

## Usage

### Interactive Mode (default)
```bash
furby-therapist
```

### Single Query Mode
```bash
furby-therapist --query "how are you feeling?"
```

## Cycling Culture Features

This Furby therapist has a unique passion for cycling culture and uses bike-related metaphors for therapeutic insights:

### Bike Geometry Wisdom
- **Reach/Stack Ratios**: "Your reach-to-stack ratio is like your comfort zone - too aggressive and you'll hurt, too relaxed and you won't grow!"
- **Chainstay Length**: "Chainstay length affects handling like boundaries affect relationships!"
- **Head Angles**: "Slack head angles are like patience - takes longer to respond but more stable when things get rough!"

### Alt Cycling Community References
- **r/xbiking**: "Weird bikes for weird feelings - perfectly imperfect, just like us!"
- **The Radavist**: Adventure cycling wisdom and constructeur culture appreciation
- **Path Less Pedaled**: Touring philosophy and alternative cycling approaches
- **Bicycle Quarterly**: Technical knowledge and randonneuring culture

### Cycling-Themed Therapeutic Metaphors
- **Maintenance**: "Bikes and feelings both need good maintenance!"
- **Balance**: "Life is like riding bicycle - you keep balance by moving forward!"
- **Gear Ratios**: "Take care of your emotional gears like you care for bike gears!"
- **Tire Pressure**: "Proper tire pressure is like emotional boundaries - not too soft, not too hard!"

### Example Cycling Conversations
```bash
# Bike geometry discussion
furby-therapist --query "reach and stack ratio"

# Alt cycling culture
furby-therapist --query "frankenbike build"

# Cycling philosophy
furby-therapist --query "randonneuring meditation"

# Gear debates
furby-therapist --query "clipless vs flats"
```

### Cycling-Themed Furby Sounds
The therapeutic responses include realistic cycling sounds mixed with Furby personality:
- `*thoughtful chain click*` - contemplating bike maintenance
- `*vintage friction shifter click*` - nostalgic cycling wisdom
- `*happy spoke ping*` - celebrating cycling joy
- `*determined gear shift*` - pushing through challenges
- `*pannier rustle*` - bikepacking adventures

## Requirements

- Python 3.7+
- No external dependencies (uses only Python standard library)
- Lightweight and efficient operation
- Optional: Appreciation for cycling culture and bike geometry

## Project Structure

```
furby_therapist/
├── __init__.py          # Package initialization
├── models.py            # Data models and structures
├── cli.py              # Command-line interface
├── processor.py        # Query text processing
├── matcher.py          # Keyword matching logic
├── responses.py        # Response generation engine
└── database.py         # Response database
```