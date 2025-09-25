"""
Error handling and logging utilities for the Furby Therapist CLI.
Provides comprehensive error handling with Furby-style user messages and detailed logging.
"""

import logging
import os
import sys
import traceback
from datetime import datetime
from pathlib import Path
from typing import Optional, Any, Dict, List
from functools import wraps

# Optional psutil import for memory monitoring
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

from ..models import FurbyResponse


class FurbyErrorHandler:
    """Centralized error handling with Furby personality and comprehensive logging."""
    
    def __init__(self, log_level: str = "INFO", log_file: Optional[str] = None):
        """Initialize error handler with logging configuration."""
        self.setup_logging(log_level, log_file)
        self.logger = logging.getLogger(__name__)
        
        # Memory monitoring thresholds (in MB)
        self.memory_warning_threshold = 40  # 40MB warning
        self.memory_critical_threshold = 50  # 50MB critical
        
        # Error message templates with Furby personality
        self.furby_error_messages = {
            'file_not_found': "*worried beep* Ooh no! Furby can't find that file! {filename} seems to be missing! *gentle chirp*",
            'json_decode_error': "*confused chirp* Ooh! Furby's brain got mixed up reading that file! The format looks funny! *supportive beep*",
            'memory_warning': "*concerned purr* Furby is using lots of memory! Me try to clean up! *gentle whirr*",
            'memory_critical': "*urgent beep* Ooh no! Furby's memory is almost full! Me need to rest! *worried chirp*",
            'processing_error': "*apologetic chirp* Oops! Furby had a little hiccup processing that! But me still here for you! *supportive purr*",
            'validation_error': "*gentle beep* Ooh! That input looks a bit funny to Furby! Try again? *encouraging chirp*",
            'network_error': "*understanding purr* Furby works offline only! No internet needed! *reassuring chirp*",
            'permission_error': "*sad beep* Furby doesn't have permission to do that! Check file permissions? *helpful chirp*",
            'timeout_error': "*patient purr* That took longer than expected! Furby is still thinking! *gentle beep*",
            'unknown_error': "*confused but supportive chirp* Something unexpected happened, but Furby is still here! *warm purr*"
        }
    
    def setup_logging(self, log_level: str, log_file: Optional[str] = None) -> None:
        """Setup comprehensive logging system."""
        # Create logs directory if it doesn't exist
        log_dir = Path.home() / '.furby_therapist' / 'logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Default log file with timestamp
        if log_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = log_dir / f"furby_therapist_{timestamp}.log"
        
        # Configure logging format
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        # Setup file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(log_format))
        
        # Setup console handler (only for warnings and errors to not interfere with UX)
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
        
        # Configure root logger
        logging.basicConfig(
            level=getattr(logging, log_level.upper()),
            handlers=[file_handler, console_handler],
            format=log_format
        )
    
    def get_furby_error_message(self, error_type: str, **kwargs) -> str:
        """Get a Furby-style error message for the given error type."""
        template = self.furby_error_messages.get(error_type, self.furby_error_messages['unknown_error'])
        try:
            return template.format(**kwargs)
        except KeyError:
            return self.furby_error_messages['unknown_error']
    
    def log_error(self, error: Exception, context: str = "", user_input: str = "") -> str:
        """Log error with full context and return user-friendly Furby message."""
        error_type = type(error).__name__
        error_message = str(error)
        
        # Log detailed error information
        self.logger.error(f"Error in {context}: {error_type}: {error_message}")
        self.logger.error(f"User input: {user_input}")
        self.logger.error(f"Traceback: {traceback.format_exc()}")
        
        # Log system information for debugging
        self.log_system_info()
        
        # Return appropriate Furby message based on error type
        if isinstance(error, FileNotFoundError):
            return self.get_furby_error_message('file_not_found', filename=getattr(error, 'filename', 'unknown'))
        elif isinstance(error, PermissionError):
            return self.get_furby_error_message('permission_error')
        elif isinstance(error, (ValueError, TypeError)) and 'json' in error_message.lower():
            return self.get_furby_error_message('json_decode_error')
        elif isinstance(error, TimeoutError):
            return self.get_furby_error_message('timeout_error')
        elif isinstance(error, (ConnectionError, OSError)) and 'network' in error_message.lower():
            return self.get_furby_error_message('network_error')
        elif isinstance(error, (ValueError, TypeError)):
            return self.get_furby_error_message('validation_error')
        else:
            return self.get_furby_error_message('processing_error')
    
    def log_system_info(self) -> None:
        """Log current system resource usage for debugging."""
        if not PSUTIL_AVAILABLE:
            self.logger.debug("psutil not available, skipping system info logging")
            return
            
        try:
            process = psutil.Process()
            memory_info = process.memory_info()
            memory_mb = memory_info.rss / 1024 / 1024
            
            self.logger.info(f"Memory usage: {memory_mb:.2f} MB")
            self.logger.info(f"CPU percent: {process.cpu_percent():.2f}%")
            
            # Log memory warning if approaching limits
            if memory_mb > self.memory_warning_threshold:
                self.logger.warning(f"Memory usage high: {memory_mb:.2f} MB (threshold: {self.memory_warning_threshold} MB)")
                
        except Exception as e:
            self.logger.debug(f"Could not log system info: {e}")
    
    def check_memory_usage(self) -> Optional[str]:
        """Check current memory usage and return warning message if needed."""
        if not PSUTIL_AVAILABLE:
            self.logger.debug("psutil not available, skipping memory check")
            return None
            
        try:
            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024
            
            if memory_mb > self.memory_critical_threshold:
                self.logger.critical(f"Critical memory usage: {memory_mb:.2f} MB")
                return self.get_furby_error_message('memory_critical')
            elif memory_mb > self.memory_warning_threshold:
                self.logger.warning(f"High memory usage: {memory_mb:.2f} MB")
                return self.get_furby_error_message('memory_warning')
                
        except Exception as e:
            self.logger.debug(f"Could not check memory usage: {e}")
        
        return None
    
    def cleanup_resources(self) -> None:
        """Perform resource cleanup and garbage collection."""
        import gc
        
        try:
            # Force garbage collection
            collected = gc.collect()
            self.logger.info(f"Garbage collection freed {collected} objects")
            
            # Log memory usage after cleanup
            self.log_system_info()
            
        except Exception as e:
            self.logger.error(f"Error during resource cleanup: {e}")


def error_handler(error_handler_instance: FurbyErrorHandler, context: str = ""):
    """Decorator for automatic error handling with Furby personality."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Extract user input if available in args/kwargs
                user_input = ""
                if args and isinstance(args[0], str):
                    user_input = args[0][:100]  # Limit length for logging
                
                # Log error and get user-friendly message
                furby_message = error_handler_instance.log_error(e, context, user_input)
                
                # Check memory usage
                memory_warning = error_handler_instance.check_memory_usage()
                if memory_warning:
                    furby_message += f"\n\n{memory_warning}"
                
                # Return error response in expected format
                if hasattr(func, '__annotations__') and func.__annotations__.get('return') == FurbyResponse:
                    # Return FurbyResponse for response engine methods
                    return FurbyResponse(
                        base_message=furby_message,
                        furby_sounds=["*worried beep*", "*supportive chirp*"],
                        furbish_phrase=("Dah koh-koh", "it's okay"),
                        formatted_output=furby_message
                    )
                else:
                    # Return string for other methods
                    return furby_message
        
        return wrapper
    return decorator


def validate_input(input_text: str, max_length: int = 1000, min_length: int = 0) -> tuple[bool, Optional[str]]:
    """
    Validate user input with Furby-style error messages.
    
    Args:
        input_text: Text to validate
        max_length: Maximum allowed length
        min_length: Minimum required length
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if input_text is None:
        return False, "*gentle beep* Furby didn't get any input! Try typing something! *encouraging chirp*"
    
    if not isinstance(input_text, str):
        return False, "*confused chirp* Ooh! That doesn't look like text to Furby! *helpful beep*"
    
    if len(input_text) > max_length:
        return False, f"*overwhelmed beep* Whoa! That's a lot of text! Furby can handle up to {max_length} characters! *gentle purr*"
    
    if len(input_text.strip()) < min_length:
        return False, "*patient chirp* Furby needs a bit more to work with! Try saying a little more! *supportive beep*"
    
    # Check for potentially harmful content (basic safety)
    harmful_patterns = ['<script', '<?php', 'javascript:', 'data:']
    if any(pattern in input_text.lower() for pattern in harmful_patterns):
        return False, "*protective beep* Ooh! That looks like computer code! Furby only understands feelings and thoughts! *caring chirp*"
    
    return True, None


def safe_file_operation(operation_name: str):
    """Decorator for safe file operations with proper error handling."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except FileNotFoundError as e:
                logging.error(f"File not found in {operation_name}: {e}")
                raise FileNotFoundError(f"Required file missing for {operation_name}: {e.filename}")
            except PermissionError as e:
                logging.error(f"Permission denied in {operation_name}: {e}")
                raise PermissionError(f"Cannot access file for {operation_name}: {e}")
            except OSError as e:
                logging.error(f"OS error in {operation_name}: {e}")
                raise OSError(f"System error during {operation_name}: {e}")
            except Exception as e:
                logging.error(f"Unexpected error in {operation_name}: {e}")
                raise RuntimeError(f"Unexpected error in {operation_name}: {e}")
        
        return wrapper
    return decorator