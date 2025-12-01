"""
Custom application exceptions for better error handling and tracing.

These exceptions provide a consistent way to handle errors across the application,
with proper HTTP status codes and error messages.
"""


class AppError(Exception):
    """
    Base exception for all application errors.
    
    Attributes:
        message: Human-readable error message
        status_code: HTTP status code to return
        payload: Additional error context (optional)
    """
    
    def __init__(self, message: str, status_code: int = 500, payload: dict = None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload or {}
    
    def to_dict(self) -> dict:
        """Convert exception to dictionary for JSON response."""
        error_dict = {'message': self.message}
        if self.payload:
            error_dict.update(self.payload)
        return error_dict


class NotFoundError(AppError):
    """
    Raised when a requested resource is not found.
    Returns HTTP 404.
    """
    
    def __init__(self, message: str = "Resource not found", payload: dict = None):
        super().__init__(message, status_code=404, payload=payload)


class ValidationError(AppError):
    """
    Raised when input validation fails.
    Returns HTTP 400.
    """
    
    def __init__(self, message: str = "Validation error", errors: list = None, payload: dict = None):
        _payload = payload or {}
        if errors:
            _payload['errors'] = errors
        super().__init__(message, status_code=400, payload=_payload)


class UnauthorizedError(AppError):
    """
    Raised when authentication is required but missing or invalid.
    Returns HTTP 401.
    """
    
    def __init__(self, message: str = "Unauthorized", payload: dict = None):
        super().__init__(message, status_code=401, payload=payload)


class ForbiddenError(AppError):
    """
    Raised when the user is authenticated but lacks permission.
    Returns HTTP 403.
    """
    
    def __init__(self, message: str = "Forbidden", payload: dict = None):
        super().__init__(message, status_code=403, payload=payload)


class ConflictError(AppError):
    """
    Raised when there's a conflict with existing data (e.g., duplicate email).
    Returns HTTP 409.
    """
    
    def __init__(self, message: str = "Resource conflict", payload: dict = None):
        super().__init__(message, status_code=409, payload=payload)


class BadRequestError(AppError):
    """
    Raised when the request is malformed or contains invalid data.
    Returns HTTP 400.
    """
    
    def __init__(self, message: str = "Bad request", payload: dict = None):
        super().__init__(message, status_code=400, payload=payload)


class InternalServerError(AppError):
    """
    Raised for unexpected server errors.
    Returns HTTP 500.
    """
    
    def __init__(self, message: str = "Internal server error", payload: dict = None):
        super().__init__(message, status_code=500, payload=payload)
