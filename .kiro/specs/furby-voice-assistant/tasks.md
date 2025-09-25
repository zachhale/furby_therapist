# Implementation Plan

- [x] 1. Set up project structure and core data models
  - Create directory structure for the Furby therapist CLI project
  - Define data classes for QueryAnalysis, ResponseCategory, and FurbyResponse
  - Create basic project configuration and requirements file
  - _Requirements: 1.1, 1.2_

- [x] 2. Create JSON response database with Furby content
  - Design JSON schema for categorized therapeutic responses
  - Create JSON file with authentic Furby phrases and sound effects
  - Include Furbish vocabulary with English translations in JSON structure
  - Implement JSON loading and validation functions in Python
  - Add sample responses across different emotional categories
  - _Requirements: 2.1, 2.5, 2.6_

- [x] 3. Build query processor for text normalization
  - Implement text normalization functions (lowercase, punctuation removal)
  - Create keyword extraction logic for identifying meaningful terms
  - Add simple emotion detection based on keyword presence
  - Write unit tests for text processing functions
  - _Requirements: 2.1, 2.10_

- [x] 4. Create keyword matcher for response categorization
  - Implement keyword matching algorithm using string containment
  - Add weighted scoring system for match confidence
  - Create fallback logic for unmatched queries
  - Write unit tests for matching accuracy and edge cases
  - _Requirements: 2.1, 2.9_

- [x] 5. Develop response engine with Furby personality
  - Implement response selection based on category and emotion
  - Add Furby-style language formatting and sound effects
  - Create logic for randomly including Furbish phrases with translations
  - Apply therapeutic framing to responses while maintaining Furby charm
  - Write unit tests for response generation and formatting
  - _Requirements: 2.1, 2.2, 2.4, 2.5, 2.6, 2.7, 2.8_

- [x] 5.1 Add repeat functionality to response engine
  - Implement response caching to store both the original Furby response and a clean version without Furbish phrases
  - Cache the base therapeutic message separately from Furby sounds and Furbish translations
  - Add detection for repeat requests (keywords like "repeat", "say again", "what did you say")
  - Create repeat response method that returns the cached clean version without Furbish phrases or excessive Furby sounds
  - Ensure repeat responses maintain all therapeutic content while being more accessible and clear
  - Write unit tests for repeat functionality, caching structure, and Furbish removal
  - _Requirements: 2.2, 2.6_

- [x] 5.2 Add bicycle-themed easter eggs
  - Create bicycle keyword detection for terms like "bike", "bicycle", "cycling", "riding", "pedal", "chain", "wheel", "maintenance"
  - Add special bicycle-themed Furby responses with bike puns and cycling humor
  - Include therapeutic bicycle metaphors (life balance, moving forward, overcoming hills, etc.)
  - Create bicycle-specific Furbish phrases with cycling translations
  - Reference cycling memes and community humor from https://bcc-wiki.herokuapp.com/memes-lulz-copypastas for inspiration
  - Include bike joke reference from https://callinginsickmag.com/cdn/shop/files/1_sticker_donttalktome.jpg?v=1750440393&width=1680
  - Ensure easter eggs maintain therapeutic value while adding personality and humor
  - Write unit tests for bicycle keyword detection and themed response generation
  - _Requirements: 2.2, 2.4, 2.5_

- [x] 5.3 Verify and align all Furbish phrases with authentic Furbish language
  - Research authentic Furbish vocabulary from original 1998 Furby documentation and community resources
  - Audit all existing Furbish phrases in responses.json for accuracy against official Furbish dictionary
  - Correct any non-authentic or invented Furbish phrases to use proper Furbish words and grammar
  - Ensure Furbish phrase structure follows authentic patterns (word order, syllable patterns, phonetics)
  - Verify that English translations accurately reflect the Furbish meanings
  - Add authentic Furbish alternatives for any phrases that cannot be directly translated
  - Update bicycle-themed Furbish phrases to use authentic Furbish vocabulary where possible
  - Create reference documentation of all Furbish phrases used with their authentic sources
  - Write unit tests to validate Furbish phrase authenticity and proper formatting
  - _Requirements: 2.5, 2.6_

- [x] 6. Build CLI interface with dual modes
  - Create main CLI entry point that defaults to long-running interactive mode
  - Implement continuous conversation loop with persistent prompt for interactive mode
  - Add command-line argument parsing to support non-interactive single query mode (e.g., --query "how are you?")
  - Create consistent output formatting for Furby responses in both modes
  - _Requirements: 3.1, 3.3, 3.4, 3.5, 3.7_

- [x] 7. Integrate components into complete pipeline
  - Wire together query processor, keyword matcher, and response engine
  - Implement end-to-end query processing from CLI input to Furby response
  - Add error handling throughout the pipeline with Furby-style error messages
  - Test complete workflow with various input scenarios
  - _Requirements: 3.1, 3.2, 4.1, 4.4_

- [x] 8. Enhance interactive mode and user experience
  - Implement robust continuous input loop as the primary CLI mode
  - Add graceful exit handling for Ctrl+C and quit commands (quit, exit, bye)
  - Create welcoming Furby-style startup message and usage instructions
  - Add persistent conversation prompt and session management
  - Include conversation history context for more natural interactions
  - _Requirements: 3.5, 3.6_

- [x] 9. Implement good morning/good night greetings with authentic Furbish
  - Replace generic hello messages with "good morning" greetings when starting up the CLI
  - Replace generic goodbye messages with "good night" greetings when ending the chat
  - Create good morning messages in English and authentic Furbish (e.g., "noo-loo koh-koh" - "happy wake")
  - Create good night messages in English and authentic Furbish (e.g., "koh-koh may-may" - "sleep love")
  - Update startup welcome message to use good morning greeting instead of generic hello
  - Update shutdown goodbye message to use good night greeting instead of generic goodbye
  - Ensure all Furbish phrases use authentic vocabulary from the official dictionary
  - Write unit tests for greeting message generation and Furbish authenticity
  - _Requirements: 2.5, 2.6, 3.5, 3.6_



- [x] 10. Implement comprehensive error handling
  - Add input validation with friendly Furby-style error messages
  - Implement graceful fallbacks when keyword matching fails
  - Add logging system for debugging while maintaining user experience
  - Create resource cleanup and memory management safeguards
  - _Requirements: 4.1, 4.4, 4.5_

- [x] 11. Expand bicycle humor with cycling culture references
  - Add jokes and references about alternative cycling culture (alt cycling, gravel grinding, bikepacking)
  - Include humor about r/xbiking community topics (weird bikes, frankenbikes, rigid MTBs on road, etc.)
  - Add jokes referencing Bicycle Quarterly magazine topics (randonneuring, vintage bikes, tire pressure debates)
  - Include references to Calling in Sick magazine culture and bike messenger humor
  - Create Furby-style commentary on cycling gear debates (clipless vs flats, carbon vs steel, etc.)
  - Add therapeutic cycling metaphors that reference these communities
  - Ensure all cycling humor maintains the supportive therapeutic tone
  - Write unit tests for expanded cycling keyword detection and themed responses
  - _Requirements: 2.2, 2.4, 2.5_

- [x] 12. Create cycling mode toggle with --bikes flag
  - Add --bikes command-line flag to enable cycling mode in both interactive and single-query modes
  - Keep existing therapeutic responses as the default standard mode (no cycling humor)
  - Remove bicycle category as a special priority case in the matcher to allow emotional categories to take precedence
  - Remove bicycle keyword priority matching logic that overrides emotional category detection
  - Create cycling-enhanced versions of all emotional response categories that activate only with --bikes flag, following existing sophisticated cycling themes:
    - Cycling sadness responses with alt cycling culture (e.g., "sadness is like a broken spoke - fixable but needs patience, just like r/xbiking teaches us")
    - Cycling anxiety responses with bike geometry wisdom (e.g., "anxiety affects your emotional reach-to-stack ratio - find your comfort zone")
    - Cycling anger responses with gravel grinding metaphors (e.g., "anger is like rough gravel - builds character if you lean into it")
    - Cycling happiness responses with randonneuring joy (e.g., "happiness is like a perfect brevet - long, challenging, but deeply satisfying")
    - Cycling confusion responses with bike fit analogies (e.g., "confusion is like poor bike fit - small adjustments make huge differences")
    - Cycling loneliness responses with bikepacking wisdom (e.g., "loneliness teaches self-reliance like solo bikepacking adventures")
    - Cycling gratitude responses with constructeur appreciation (e.g., "gratitude is like hand-built frames - crafted with care and built to last")
    - Cycling general and fallback responses featuring The Radavist, Path Less Pedaled, Bicycle Quarterly references, N+1 rule jokes, bike geometry humor (wheelbase, BB drop, trail, slack vs steep angles), and retrogrouch wisdom
  - Integrate existing bicycle category responses into the cycling-enhanced emotional categories
  - Add N+1 rule jokes throughout different emotional contexts when in cycling mode (e.g., "you need N+1 coping strategies")
  - Update CLI help text to explain both standard and cycling modes
  - Ensure all cycling metaphors maintain therapeutic value and emotional appropriateness
  - Update tests to verify both standard mode (no cycling) and cycling mode (--bikes flag) work correctly
  - Write unit tests to verify cycling humor only appears when --bikes flag is used
  - _Requirements: 2.2, 2.4, 2.5, 2.7, 3.1, 3.3_

- [x] 13. Refactor response generation into reusable library
  - Create a clean library interface that separates response generation logic from CLI-specific code
  - Design a FurbyTherapist class that encapsulates all response generation functionality
  - Implement library methods for single query processing with cycling mode support
  - Create library initialization that accepts cycling_mode parameter for bikes flag functionality
  - Separate CLI-specific logic (argument parsing, interactive mode, formatting) from core response generation
  - Refactor CLI to use the new library interface while maintaining all existing functionality
  - Ensure library can be imported and used independently without CLI dependencies
  - Create library methods for:
    - Processing single queries with optional cycling mode
    - Getting available response categories
    - Accessing conversation history and session management
    - Retrieving good morning/good night greetings
    - Managing repeat functionality
  - Design library interface to be stateful (maintains conversation context) or stateless (single query processing)
  - Write unit tests for the library interface to ensure it works independently of CLI
  - Update existing CLI tests to verify they still work with the refactored architecture
  - Create example usage documentation showing how to use the library programmatically
  - _Requirements: 1.1, 1.3, 2.1, 2.2, 3.1, 3.3_

- [x] 14. Reorganize project structure for three-function architecture
  - Design project structure to support three distinct functions:
    1. **Core Library**: Importable library for external projects (furby_therapist.core or furby_therapist.lib)
    2. **CLI Interface**: Command-line tool that imports and uses the library (furby_therapist.cli)
    3. **Future Voice Interface**: Prepare structure for upcoming voice-enabled chatbot project (separate project that will import this library)
  - Create proper Python package structure following standard conventions:
    - `furby_therapist/` (main package)
    - `furby_therapist/core/` or `furby_therapist/lib/` (core library components)
    - `furby_therapist/cli/` (CLI-specific code)
    - `furby_therapist/models/` (shared data models)
    - `furby_therapist/data/` (JSON files, resources)
  - Separate core library components from CLI-specific code into distinct modules
  - Move CLI entry point and argument parsing to dedicated cli module
  - Organize library components into logical submodules (processor, matcher, responses, etc.)
  - Create clean public API surface in main `__init__.py` for external library usage
  - Ensure core library can be imported cleanly without any CLI dependencies
  - Design library interface to be easily consumable by future voice interface project
  - Update import statements throughout the codebase to reflect new structure
  - Move CLI-specific files (argument parsing, interactive mode, formatting) to cli package
  - Create separate entry points for library vs CLI usage in setup configuration
  - Update all tests to work with the new import structure and maintain test organization
  - Update documentation to reflect the new project organization and usage patterns
  - Follow Python packaging best practices to enable easy distribution and external consumption
  - Prepare structure to support future voice interface as a separate project that imports this library
  - _Requirements: 1.1, 1.3, 3.1_

- [x] 15. Create comprehensive test suite
  - Write unit tests for all core components (processor, matcher, engine)
  - Add integration tests for end-to-end query processing
  - Add manual test scenarios for therapeutic quality and Furby authenticity
  - _Requirements: 5.4, 5.6_

- [-] 16. Add packaging and deployment setup
  - Create setup script for easy installation
  - Add executable script for convenient CLI access
  - Create documentation for installation and usage
  - _Requirements: 1.1, 1.3, 1.4_