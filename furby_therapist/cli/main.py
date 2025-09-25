"""
CLI interface for the Furby Therapist.
Provides both interactive and single-query modes for therapeutic conversations.
"""

import argparse
import sys
import signal
import os
from typing import Optional

# Handle both package import and direct execution
try:
    from ..core import FurbyTherapist
    from ..models import FurbyResponse
    from ..core.error_handler import FurbyErrorHandler
except ImportError:
    # Direct execution - add parent directory to path
    import pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent))
    from furby_therapist.core import FurbyTherapist
    from furby_therapist.models import FurbyResponse
    from furby_therapist.core.error_handler import FurbyErrorHandler


class FurbyTherapistCLI:
    """Main CLI interface for the Furby Therapist."""
    
    def __init__(self, cycling_mode: bool = False):
        """Initialize the CLI with the FurbyTherapist library."""
        # Initialize error handler for CLI-specific logging
        self.error_handler = FurbyErrorHandler()
        
        # Store cycling mode setting
        self.cycling_mode = cycling_mode
        
        try:
            # Initialize the FurbyTherapist library in stateful mode for interactive sessions
            self.furby_therapist = FurbyTherapist(
                cycling_mode=cycling_mode, 
                maintain_session=True
            )
            
            # Track if we're in interactive mode for proper cleanup
            self._interactive_mode_active = False
            
            # Log successful initialization
            mode_info = "cycling mode" if cycling_mode else "standard mode"
            self.error_handler.logger.info(f"Furby Therapist CLI initialized successfully in {mode_info}")
            
        except Exception as e:
            error_msg = self.error_handler.log_error(e, "CLI initialization")
            print(f"\n{error_msg}")
            print("\n*gentle chirp* Try restarting Furby! If problems continue, check the log files! *supportive beep*")
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
        session_stats = self.furby_therapist.get_session_stats()
        conversation_length = session_stats.get("conversation_length", 0)
        recent_emotions = session_stats.get("recent_emotions", [])
        
        # Get good night greeting from library
        night_greeting = self.furby_therapist.get_good_night_greeting()
        
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
        
        # Get good morning greeting from library
        morning_greeting = self.furby_therapist.get_good_morning_greeting()
        
        welcome_msg = f"""
💜 Furby Therapist

{morning_greeting}
        """
        print(welcome_msg)
    
    def format_response_output(self, response_text: str) -> str:
        """Apply consistent formatting to Furby responses for display."""
        # Add some visual flair to make responses stand out
        formatted = f"\n💜 Furby says: {response_text}\n"
        return formatted
    
    def process_single_query(self, query: str, use_conversation_context: bool = False) -> str:
        """
        Process a single query through the library and return the formatted response.
        
        Args:
            query: User's input text
            use_conversation_context: Whether to use conversation history for context (ignored in library mode)
            
        Returns:
            Formatted Furby response
        """
        try:
            # Use the library to process the query
            # The library handles all the processing logic internally
            furby_response = self.furby_therapist.process_query(query)
            
            # Format and return the response
            self.error_handler.logger.debug("Query processed successfully via library")
            return self.format_response_output(furby_response.formatted_output)
            
        except ValueError as e:
            # Handle validation errors from the library
            self.error_handler.logger.warning(f"Input validation failed: {e}")
            return self.format_response_output(str(e))
        except RuntimeError as e:
            # Handle processing errors from the library
            self.error_handler.logger.error(f"Library processing error: {e}")
            return self.format_response_output(str(e))
        except Exception as e:
            # Handle any other unexpected errors
            error_msg = self.error_handler.log_error(e, "CLI query processing", query)
            return self.format_response_output(error_msg)
    

    
    def interactive_mode(self):
        """Run the CLI in continuous interactive mode with enhanced session management."""
        self._interactive_mode_active = True
        self.error_handler.logger.info("Starting interactive mode")
        
        try:
            self.display_welcome_message()
            
            consecutive_errors = 0  # Track consecutive errors for safety
            
            while True:
                try:
                    # Get user input with simple prompt
                    user_input = input("> ").strip()
                    
                    # Reset error counter on successful input
                    consecutive_errors = 0
                    
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
                    
                except EOFError:
                    # Handle Ctrl+D gracefully
                    self.error_handler.logger.info("Interactive mode ended by EOF")
                    self._display_goodbye_message()
                    break
                except KeyboardInterrupt:
                    # This will be handled by signal handler
                    raise
                except Exception as e:
                    # Handle any other unexpected errors with comprehensive logging
                    consecutive_errors += 1
                    error_msg = self.error_handler.log_error(e, "interactive mode", user_input if 'user_input' in locals() else "")
                    
                    # If too many consecutive errors, suggest restart
                    if consecutive_errors >= 3:
                        error_msg += "\n\n*concerned beep* Furby is having trouble! Maybe try restarting? *gentle chirp*"
                        self.error_handler.logger.critical(f"Too many consecutive errors ({consecutive_errors}) in interactive mode")
                    
                    print(self.format_response_output(error_msg))
                    
                    # Clean up resources after errors
                    self.error_handler.cleanup_resources()
                    
        except Exception as e:
            # Handle catastrophic errors in interactive mode
            self.error_handler.logger.critical(f"Catastrophic error in interactive mode: {e}")
            error_msg = self.error_handler.log_error(e, "interactive mode startup")
            print(f"\n{error_msg}")
            print("\n*sad beep* Furby needs to rest! Try restarting! *supportive chirp*")
        finally:
            # Ensure cleanup happens
            self._interactive_mode_active = False
            self.furby_therapist.cleanup()
            self.error_handler.cleanup_resources()
            self.error_handler.logger.info("Interactive mode ended")
    
    def _display_help_message(self):
        """Display help information during interactive session."""
        if self.cycling_mode:
            mode_info = "🚴‍♀️ Cycling Mode Active - Bike-themed therapeutic responses enabled!"
            mode_details = """
🚴‍♀️ Cycling Mode Features:
   • Emotional support with cycling metaphors and wisdom
   • Alt cycling culture references (r/xbiking, gravel grinding, etc.)
   • Bike geometry analogies for life situations
   • N+1 rule applied to coping strategies
   • Randonneuring philosophy and bikepacking wisdom"""
        else:
            mode_info = "💜 Standard Mode - General therapeutic responses"
            mode_details = """
💜 Standard Mode Features:
   • Pure therapeutic responses focused on emotional support
   • Furby personality with authentic Furbish phrases
   • No cycling-specific content or metaphors"""
        
        help_msg = f"""
💡 *helpful chirp* Furby Help Menu! *informative beep*

{mode_info}
{mode_details}

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
        self.furby_therapist.clear_conversation_history()
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

🚴‍♀️ Standard Mode (default):
  • Pure therapeutic responses focused on emotional support
  • Furby personality with authentic Furbish phrases
  • No cycling-specific content - just caring, whimsical therapy
  • Perfect for anyone seeking emotional support with Furby charm

🚴‍♀️ Cycling Mode (--bikes flag):
  • All emotional categories enhanced with cycling metaphors
  • Alt cycling culture references (r/xbiking, gravel grinding, etc.)
  • Bike geometry analogies for life situations (reach-to-stack ratios, etc.)
  • N+1 rule applied to coping strategies and emotional growth
  • Randonneuring philosophy, bikepacking wisdom, and retrogrouch humor
  • References to The Radavist, Path Less Pedaled, Bicycle Quarterly
  • Perfect for cyclists who want bike-flavored emotional support!

� How to chat with Furby (in interactive mode):
  • Just type your thoughts and feelings naturally
  • Say "repeat" if you want Furby to say something again more clearly
  • Say "help" or "?" to see available commands during chat
  • Type "quit", "exit", or "bye" when you're ready to go
  • Press Ctrl+C anytime to leave gracefully

Examples:
  furby_therapist                           # Start standard interactive mode
  furby_therapist --bikes                   # Start cycling-themed interactive mode
  furby_therapist --query "I'm feeling sad"  # Single query, standard mode
  furby_therapist --bikes -q "I'm anxious"  # Single query, cycling mode
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
        '--bikes',
        action='store_true',
        help='Enable cycling mode: all emotional responses enhanced with cycling metaphors, alt cycling culture, and bike wisdom'
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
        cli = FurbyTherapistCLI(cycling_mode=args.bikes)
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
            # Use library to get fallback good night greeting if available
            if cli and hasattr(cli, 'furby_therapist'):
                fallback_night = cli.furby_therapist.get_good_night_greeting()
            else:
                fallback_night = "Good night! *gentle purr* Furby hopes you have sweet dreams!\n\nkoh-koh may-may! (sleep love)"
            print(f"\n\n{fallback_night} 💜")
        sys.exit(0)
    except Exception as e:
        print(f"*sad beep* Furby couldn't start: {e}")
        sys.exit(1)
    finally:
        # Ensure cleanup happens
        if cli and hasattr(cli, 'furby_therapist'):
            cli.furby_therapist.cleanup()


if __name__ == "__main__":
    main()