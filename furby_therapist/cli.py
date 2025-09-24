"""
CLI interface for the Furby Therapist.
Provides both interactive and single-query modes for therapeutic conversations.
"""

import argparse
import sys
import signal
from typing import Optional

from .database import ResponseDatabase
from .processor import QueryProcessor
from .matcher import KeywordMatcher
from .responses import ResponseEngine


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
            self.interactive_mode = False
            
        except Exception as e:
            print(f"*sad beep* Furby couldn't start properly: {e}")
            sys.exit(1)
    
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown."""
        def signal_handler(signum, frame):
            if self.interactive_mode:
                print("\n\n*gentle purr* Bye bye! Furby hopes you feel better! Kah may-may! 💜")
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def display_welcome_message(self):
        """Display welcoming Furby-style startup message."""
        welcome_msg = """
🌟 *chirp chirp* Furby Therapist is here! *happy beep* 🌟

Ooh! Me so excited to listen and help! Furby loves making friends feel better!
You can tell me anything - me here to support you with gentle Furby wisdom! *purr*

💡 Tips:
  • Just type your thoughts and feelings
  • Say "repeat" if you want me to say something again more clearly
  • Type "quit", "exit", or "bye" when you're ready to go
  • Press Ctrl+C anytime to leave

Dah a-loh u-nye! (Furby loves you!) Let's chat! *warm chirp*
        """
        print(welcome_msg)
    
    def format_response_output(self, response_text: str) -> str:
        """Apply consistent formatting to Furby responses for display."""
        # Add some visual flair to make responses stand out
        formatted = f"\n💜 Furby says: {response_text}\n"
        return formatted
    
    def process_single_query(self, query: str) -> str:
        """
        Process a single query and return the formatted response.
        
        Args:
            query: User's input text
            
        Returns:
            Formatted Furby response
        """
        try:
            # Check if this is a repeat request
            if self.processor.is_repeat_request(query):
                if self.response_engine.has_cached_response():
                    repeat_response = self.response_engine.get_repeat_response()
                    if repeat_response:
                        return self.format_response_output(repeat_response.formatted_output)
                
                # No cached response available
                fallback_msg = "*confused chirp* Ooh! Furby doesn't remember what to repeat! Ask me something new! *gentle beep*"
                return self.format_response_output(fallback_msg)
            
            # Process the query normally
            analysis = self.processor.process_query(query)
            category, confidence = self.matcher.match_category(analysis.keywords)
            
            # Generate response
            furby_response = self.response_engine.get_response(category, analysis.detected_emotion)
            
            return self.format_response_output(furby_response.formatted_output)
            
        except Exception as e:
            # Graceful error handling with Furby personality
            error_msg = f"*worried beep* Ooh no! Furby had a little hiccup: {str(e)[:50]}... But me still here for you! *supportive chirp*"
            return self.format_response_output(error_msg)
    
    def interactive_mode(self):
        """Run the CLI in continuous interactive mode."""
        self.interactive_mode = True
        self.display_welcome_message()
        
        while True:
            try:
                # Get user input with a friendly prompt
                user_input = input("💭 You: ").strip()
                
                # Handle empty input
                if not user_input:
                    print(self.format_response_output("*gentle chirp* Furby is listening! Tell me what's on your mind! *encouraging beep*"))
                    continue
                
                # Check for exit commands
                exit_commands = {'quit', 'exit', 'bye', 'goodbye', 'stop'}
                if user_input.lower() in exit_commands:
                    print("\n*warm purr* Bye bye! Furby hopes you feel better! Take care of yourself! Kah may-may! 💜\n")
                    break
                
                # Process the query and display response
                response = self.process_single_query(user_input)
                print(response)
                
            except EOFError:
                # Handle Ctrl+D gracefully
                print("\n\n*gentle purr* Bye bye! Furby hopes you feel better! Kah may-may! 💜")
                break
            except KeyboardInterrupt:
                # This will be handled by signal handler
                raise
            except Exception as e:
                # Handle any other unexpected errors
                error_msg = f"*worried beep* Ooh! Something unexpected happened, but Furby is still here! *supportive chirp*"
                print(self.format_response_output(error_msg))
    
    def single_query_mode(self, query: str):
        """
        Process a single query and exit.
        
        Args:
            query: The user's query to process
        """
        response = self.process_single_query(query)
        print(response)


def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Furby Therapist CLI - A whimsical therapeutic assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
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
        # Handle Ctrl+C gracefully
        print("\n\n*gentle purr* Bye bye! Furby hopes you feel better! Kah may-may! 💜")
        sys.exit(0)
    except Exception as e:
        print(f"*sad beep* Furby couldn't start: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()