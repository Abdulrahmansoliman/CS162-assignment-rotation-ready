"""
Email Service Exceptions

Custom exceptions for email-related errors.
"""


class EmailError(Exception):
    """Base exception for email-related errors."""
    
    def __init__(self, message: str, original_error: Exception = None):
        super().__init__(message)
        self.message = message
        self.original_error = original_error
    
    def __str__(self):
        if self.original_error:
            return f"{self.message}: {str(self.original_error)}"
        return self.message


class EmailConfigurationError(EmailError):
    """Raised when email configuration is invalid or missing."""
    pass


class EmailDeliveryError(EmailError):
    """Raised when email delivery fails."""
    pass


class EmailTemplateError(EmailError):
    """Raised when email template rendering fails."""
    pass
