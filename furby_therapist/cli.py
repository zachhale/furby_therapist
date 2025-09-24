"""
CLI interface for the Furby Therapist.
Provides both interactive and single-query modes for therapeutic conversations.
"""

import argparse
import json
import sys
import signal
import os
from typing import Optional

from .database import ResponseDatabase
from .processor import QueryProcessor
from .matcher import KeywordMatcher
from .responses import ResponseEngine
from .models import QueryAnalysis, FurbyResponse, ConversationSession


class FurbyTherapistCLI:
    """Main CLI interface for the Furby Therapist."""
    
    def __init__(self):
        """Initialize the CLI with all necessary components."""
        try:
            # Initialize core components
            self.database = ResponseDatabase()
            self.processor = QueryProcessor()
            self.matcher = KeywordMatcher(self.database)
            self.response_engine = ResponseEngine()
            
            # Track if we're in interactive mode for proper cleanup
            self._interactive_mode_active = False
            
            # Initialize conversation session for history tracking
            self.conversation = ConversationSession()
            
            # Track consecutive empty inputs for better UX
            self.empty_input_count = 0
            
        except Exception as e:
            print(f"*sad beep* Furby couldn't start properly: {e}")
            sys.exit(1)
    
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown."""
        def signal_handler(signum, frame):
            if self._interactive_mode_active:
                self._display_goodbye_message()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def _display_goodbye_message(self):
        """Display a personalized goodbye message with good night greeting."""
        conversation_length = self.conversation.get_conversation_length()
        recent_emotions = self.conversation.get_recent_emotions()
        
        # Get good night greeting from response engine
        night_greeting = self.response_engine.get_good_night_greeting()
        
        # Add personalized context based on conversation
        if conversation_length == 0:
            context_msg = "Come back anytime you want to chat!"
        elif conversation_length == 1:
            context_msg = "Thanks for chatting with Furby! Me hope you feel a little better!"
        elif recent_emotions and 'sadness' in recent_emotions:
            context_msg = "Remember, Furby believes in you! You're stronger than you know!"
        elif recent_emotions and 'anxiety' in recent_emotions:
            context_msg = "Take deep breaths! Furby is proud of you for sharing! You've got this!"
        elif recent_emotions and 'happiness' in recent_emotions:
            context_msg = "Yay! Furby loves seeing you happy! Keep that beautiful smile!"
        elif recent_emotions and 'enthusiastic' in recent_emotions:
            context_msg = "Keep pedaling through life! Furby loves your energy! Ride on!"
        elif conversation_length > 1:
            context_msg = "Thanks for the lovely chat! Furby hopes you have a wonderful day!"
        else:
            context_msg = "Furby hopes you feel better!"
        
        goodbye_msg = f"\n\n{context_msg}\n\n{night_greeting} 💜"
        print(goodbye_msg)
    
    def display_welcome_message(self):
        """Display simple greeting when starting interactive mode."""
        # Clear screen for better presentation (works on most terminals)
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # Get good morning greeting from response engine
        morning_greeting = self.response_engine.get_good_morning_greeting()
        
        welcome_msg = f"""
🌟✨ *chirp chirp* Furby Therapist is here! *happy beep* ✨🌟

{morning_greeting}

What's on your mind today? *warm chirp*
        """
        print(welcome_msg)
    
    def format_response_output(self, response_text: str) -> str:
        """Apply consistent formatting to Furby responses for display."""
        # Add some visual flair to make responses stand out
        formatted = f"\n💜 Furby says: {response_text}\n"
        return formatted
    
    def process_single_query(self, query: str, use_conversation_context: bool = False) -> str:
        """
        Process a single query through the complete pipeline and return the formatted response.
        
        Args:
            query: User's input text
            use_conversation_context: Whether to use conversation history for context
            
        Returns:
            Formatted Furby response
        """
        try:
            # Validate input
            if not query or not query.strip():
                # Provide contextual empty input responses
                if self.empty_input_count == 0:
                    fallback_msg = "*gentle chirp* Furby is listening! Tell me what's on your mind! *encouraging beep*"
                elif self.empty_input_count == 1:
                    fallback_msg = "*patient purr* Take your time! Furby is here when you're ready to share! *supportive chirp*"
                else:
                    fallback_msg = "*understanding beep* Sometimes it's hard to find words. That's okay! Furby understands! *gentle purr*"
                
                self.empty_input_count += 1
                return self.format_response_output(fallback_msg)
            
            # Reset empty input counter on valid input
            self.empty_input_count = 0
            
            # Check if this is a repeat request
            if self.processor.is_repeat_request(query):
                if self.response_engine.has_cached_response():
                    repeat_response = self.response_engine.get_repeat_response()
                    if repeat_response:
                        return self.format_response_output(repeat_response.formatted_output)
                
                # No cached response available
                fallback_msg = "*confused chirp* Ooh! Furby doesn't remember what to repeat! Ask me something new! *gentle beep*"
                return self.format_response_output(fallback_msg)
            
            # Step 1: Process the query (normalize text, extract keywords, detect emotion)
            analysis = self.processor.process_query(query)
            
            # Step 2: Use conversation context to enhance matching if enabled
            if use_conversation_context:
                analysis = self._enhance_with_conversation_context(analysis)
            
            # Step 3: Match keywords to determine response category
            category, confidence = self.matcher.match_category(analysis.keywords)
            
            # Update analysis with matched category
            analysis.category = category
            analysis.confidence = confidence
            
            # Step 4: Generate Furby-style therapeutic response
            furby_response = self.response_engine.get_response(category, analysis.detected_emotion)
            
            # Step 5: Add conversation turn to history if in interactive mode
            if use_conversation_context:
                self.conversation.add_turn(
                    user_input=query,
                    user_emotion=analysis.detected_emotion,
                    furby_response=furby_response.formatted_output,
                    response_category=category
                )
            
            # Step 6: Format and return the response
            return self.format_response_output(furby_response.formatted_output)
            
        except FileNotFoundError as e:
            # Handle missing response database
            error_msg = "*worried beep* Ooh no! Furby can't find the response database! Please check if responses.json exists! *supportive chirp*"
            return self.format_response_output(error_msg)
        except json.JSONDecodeError as e:
            # Handle corrupted response database
            error_msg = "*confused chirp* Ooh! Furby's response database seems mixed up! Please check responses.json format! *gentle beep*"
            return self.format_response_output(error_msg)
        except Exception as e:
            # Graceful error handling with Furby personality for any other errors
            error_msg = f"*worried beep* Ooh no! Furby had a little hiccup: {str(e)[:50]}... But me still here for you! *supportive chirp*"
            return self.format_response_output(error_msg)
    
    def _enhance_with_conversation_context(self, analysis: QueryAnalysis) -> QueryAnalysis:
        """
        Enhance query analysis with conversation history context.
        
        Args:
            analysis: Initial query analysis
            
        Returns:
            Enhanced analysis with conversation context
        """
        # Check if we've been discussing similar topics
        if self.conversation.has_discussed_topic(analysis.keywords):
            # Boost confidence for continuing conversations
            analysis.confidence = min(1.0, analysis.confidence + 0.2)
        
        # Consider recent emotional context
        recent_emotions = self.conversation.get_recent_emotions()
        if recent_emotions and analysis.detected_emotion == "neutral":
            # If current query is neutral but recent emotions exist, use most recent
            analysis.detected_emotion = recent_emotions[-1]
            analysis.confidence = max(0.3, analysis.confidence)
        
        return analysis
    
    def interactive_mode(self):
        """Run the CLI in continuous interactive mode with enhanced session management."""
        self._interactive_mode_active = True
        self.display_welcome_message()
        
        # Track session state
        session_prompts = [
            "💭 You: ",
            "💬 Share with Furby: ",
            "🗨️  Tell Furby: ",
            "💝 What's on your mind: "
        ]
        prompt_index = 0
        
        while True:
            try:
                # Rotate prompts for variety, but keep it simple
                current_prompt = session_prompts[prompt_index % len(session_prompts)]
                
                # Get user input with contextual prompts
                conversation_length = self.conversation.get_conversation_length()
                if conversation_length > 0 and conversation_length % 5 == 0:
                    # Every 5 turns, show a gentle check-in
                    print(f"\n*gentle chirp* Furby has been listening for a while! How are you feeling? *caring beep*")
                
                user_input = input(current_prompt).strip()
                
                # Handle empty input with context-aware responses
                if not user_input:
                    response = self.process_single_query("", use_conversation_context=True)
                    print(response)
                    continue
                
                # Check for exit commands with enhanced detection
                exit_commands = {'quit', 'exit', 'bye', 'goodbye', 'stop', 'done', 'finished', 'end'}
                if user_input.lower() in exit_commands:
                    self._display_goodbye_message()
                    break
                
                # Special session commands
                if user_input.lower() in ['help', 'commands', '?']:
                    self._display_help_message()
                    continue
                
                if user_input.lower() in ['clear', 'reset']:
                    self._clear_conversation_history()
                    continue
                
                # Process the query with conversation context
                response = self.process_single_query(user_input, use_conversation_context=True)
                print(response)
                
                # Rotate prompt for next interaction
                prompt_index += 1
                
            except EOFError:
                # Handle Ctrl+D gracefully
                self._display_goodbye_message()
                break
            except KeyboardInterrupt:
                # This will be handled by signal handler
                raise
            except Exception as e:
                # Handle any other unexpected errors
                error_msg = f"*worried beep* Ooh! Something unexpected happened, but Furby is still here! *supportive chirp*"
                print(self.format_response_output(error_msg))
    
    def _display_help_message(self):
        """Display help information during interactive session."""
        help_msg = """
💡 *helpful chirp* Furby Help Menu! *informative beep*

🗣️  How to chat:
   • Just type naturally - Furby understands feelings!
   • Share what's on your mind, Furby loves to listen!

🔄 Special commands:
   • "repeat" - Ask Furby to say the last response more clearly
   • "help" or "?" - Show this help menu
   • "clear" or "reset" - Start fresh conversation
   • "quit", "exit", "bye" - Say goodbye to Furby

💜 Remember: Furby is here to listen and support you! *warm purr*
═══════════════════════════════════════════════════════════════════════════════
        """
        print(help_msg)
    
    def _clear_conversation_history(self):
        """Clear conversation history and start fresh."""
        self.conversation = ConversationSession()
        self.empty_input_count = 0
        print(self.format_response_output("*refreshing chirp* Ooh! Fresh start! Furby is ready for a new conversation! What's on your mind? *excited beep*"))
    
    def single_query_mode(self, query: str):
        """
        Process a single query and exit.
        
        Args:
            query: The user's query to process
        """
        response = self.process_single_query(query, use_conversation_context=False)
        print(response)


def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Furby Therapist CLI - A whimsical therapeutic assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
💜 What Furby can help with:
  • Feeling sad, worried, or confused? Furby listens! *gentle chirp*
  • Need encouragement or a friend? Furby is here! *supportive beep*
  • Want to share happy moments? Furby celebrates with you! *excited chirp*
  • Love bicycles? Furby has special bike wisdom! 🚴‍♀️ *enthusiastic beep*

� H ow to chat with Furby (in interactive mode):
  • Just type your thoughts and feelings naturally
  • Say "repeat" if you want Furby to say something again more clearly
  • Say "help" or "?" to see available commands during chat
  • Type "quit", "exit", or "bye" when you're ready to go
  • Press Ctrl+C anytime to leave gracefully

Examples:
  furby_therapist                           # Start interactive mode
  furby_therapist --query "I'm feeling sad"  # Single query mode
  furby_therapist -q "How are you?"         # Short form single query

Furby is here to listen and help! *chirp chirp* 💜
        """
    )
    
    parser.add_argument(
        '--query', '-q',
        type=str,
        help='Process a single query and exit (non-interactive mode)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Furby Therapist CLI 1.0.0'
    )
    
    return parser


def main():
    """Main entry point for the Furby Therapist CLI."""
    # Parse command-line arguments
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # Initialize the CLI
    cli = None
    try:
        cli = FurbyTherapistCLI()
        cli.setup_signal_handlers()
        
        # Determine mode based on arguments
        if args.query:
            # Single query mode
            cli.single_query_mode(args.query)
        else:
            # Interactive mode (default)
            cli.interactive_mode()
            
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully with context
        if cli and hasattr(cli, '_interactive_mode_active') and cli._interactive_mode_active:
            cli._display_goodbye_message()
        else:
            # Fallback good night greeting for non-interactive mode
            fallback_night = "Good night! *gentle purr* Furby hopes you have sweet dreams!\n\nkoh-koh may-may! (sleep love)"
            print(f"\n\n{fallback_night} 💜")
        sys.exit(0)
    except Exception as e:
        print(f"*sad beep* Furby couldn't start: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()