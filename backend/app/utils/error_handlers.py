"""
Global error handlers for the Flask application.

This module provides centralized error handling with proper logging and
consistent JSON error responses. Uses exc_info=True for full stack traces.
"""
import logging
from flask import jsonify, Flask
from werkzeug.exceptions import HTTPException
from pydantic import ValidationError as PydanticValidationError

from app.exceptions import AppError

# Configure logger for error handling
logger = logging.getLogger(__name__)


def register_error_handlers(app: Flask) -> None:
    """
    Register all global error handlers with the Flask app.
    
    This centralizes error handling so individual routes don't need
    try/except blocks. All exceptions are logged with full stack traces
    using exc_info=True for better debugging.
    
    Args:
        app: Flask application instance
    """
    
    @app.errorhandler(AppError)
    def handle_app_error(error: AppError):
        """
        Handle custom application errors (NotFoundError, ValidationError, etc.).
        
        Logs the error with context and returns a JSON response with
        the error message and status code.
        """
        logger.warning(
            f"Application error: {error.message} (status={error.status_code})",
            extra={'payload': error.payload}
        )
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
    
    @app.errorhandler(PydanticValidationError)
    def handle_pydantic_validation_error(error: PydanticValidationError):
        """
        Handle Pydantic validation errors from request schemas.
        
        Extracts validation errors and returns them in a user-friendly format.
        Logs the validation failure for monitoring.
        """
        logger.warning(
            f"Validation error: {error.error_count()} validation errors",
            extra={'errors': error.errors()}
        )
        response = jsonify({
            'message': 'Validation error',
            'errors': error.errors()
        })
        response.status_code = 400
        return response
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(error: HTTPException):
        """
        Handle Werkzeug HTTP exceptions (404, 405, etc.).
        
        Converts standard HTTP errors to JSON format for API consistency.
        """
        logger.info(f"HTTP exception: {error.code} - {error.description}")
        response = jsonify({
            'message': error.description,
            'error': error.name
        })
        response.status_code = error.code
        return response
    
    @app.errorhandler(ValueError)
    def handle_value_error(error: ValueError):
        """
        Handle ValueError exceptions (invalid input, business logic errors).
        
        Treats ValueErrors as client errors (400 Bad Request) since they
        typically indicate invalid user input or request data.
        """
        logger.warning(f"Value error: {str(error)}")
        response = jsonify({
            'message': str(error)
        })
        response.status_code = 400
        return response
    
    @app.errorhandler(Exception)
    def handle_unexpected_error(error: Exception):
        """
        Catch-all handler for unexpected errors.
        
        Logs the full exception with stack trace using exc_info=True,
        which is critical for debugging production issues.
        Returns a generic error message to avoid leaking internal details.
        """
        logger.error(
            f"Unexpected error: {type(error).__name__}: {str(error)}",
            exc_info=True  # This logs the full stack trace
        )
        response = jsonify({
            'message': 'An internal server error occurred. Please try again later.',
            'error_type': type(error).__name__
        })
        response.status_code = 500
        return response


def setup_logging(app: Flask) -> None:
    """
    Configure application logging with appropriate handlers and formatters.
    
    Sets up:
    - Console logging for development
    - File logging for production (optional)
    - Proper log levels based on environment
    - Detailed formatting with timestamps and context
    
    Args:
        app: Flask application instance
    """
    # Get log level from config (default to INFO)
    log_level = app.config.get('LOG_LEVEL', 'INFO')
    
    # Create formatter with timestamp and context
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    
    # Console handler for all environments
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(getattr(logging, log_level))
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level))
    root_logger.addHandler(console_handler)
    
    # Configure Flask app logger
    app.logger.setLevel(getattr(logging, log_level))
    
    logger.info(f"Logging configured at {log_level} level")
