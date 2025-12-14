"""
Notification Service

Handles sending notifications to users (email, etc.)
Acts as a facade for the email service in the auth context.
"""

import logging
from typing import Literal

from app.services.email import EmailService


logger = logging.getLogger(__name__)


class NotificationService:
    """
    Service for sending notifications to users.
    
    Provides a simplified interface for auth-related notifications,
    delegating to the EmailService for actual delivery.
    """
    
    def __init__(self, email_service: EmailService = None):
        """
        Initialize the notification service.
        
        Args:
            email_service: Optional EmailService instance for dependency injection.
                          If not provided, will use the singleton instance.
        """
        self._email_service: EmailService = email_service
    
    @property
    def email_service(self) -> EmailService:
        """Get the email service instance."""
        if self._email_service:
            return self._email_service
        return EmailService()
    
    def send_verification_code(
        self,
        user_email: str,
        name: str,
        verification_code: str,
        expiry_minutes: int,
        code_type: Literal['registration', 'login'] = 'registration'
    ) -> None:
        """
        Send a verification code asynchronously (fire-and-forget).
        
        Returns immediately, email is sent in background thread.
        Use this for better API response times.
        
        Args:
            user_email: The recipient's email address
            name: The user's name for personalization
            verification_code: The verification code to send
            expiry_minutes: Minutes until the code expires
            code_type: Type of verification ('registration' or 'login')
        """
        def on_error(e: Exception) -> None:
            logger.error(f"[Async] Failed to send {code_type} verification to {user_email}: {e}")
        
        if code_type == 'login':
            self.email_service.send_login_code_async(
                to_email=user_email,
                name=name,
                code=verification_code,
                expiry_minutes=expiry_minutes,
                on_error=on_error
            )
        else:
            self.email_service.send_registration_code_async(
                to_email=user_email,
                name=name,
                code=verification_code,
                expiry_minutes=expiry_minutes,
                on_error=on_error
            )
    
    def send_welcome_email(self, user_email: str, name: str) -> None:
        """
        Send a welcome email asynchronously (fire-and-forget).
        
        Returns immediately, email is sent in background thread.
        
        Args:
            user_email: The recipient's email address
            name: The user's name for personalization
        """
        def on_error(e: Exception) -> None:
            logger.error(f"[Async] Failed to send welcome email to {user_email}: {e}")
        
        self.email_service.send_welcome_email_async(
            to_email=user_email,
            name=name,
            on_error=on_error
        )
    

