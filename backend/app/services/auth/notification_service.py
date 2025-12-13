"""
Notification Service

Handles sending notifications to users (email, etc.)
Acts as a facade for the email service in the auth context.
"""

import logging
from typing import Literal

from app.services.email import EmailService, EmailError


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
    ) -> bool:
        """
        Send a verification code to the user's email.
        
        Args:
            user_email: The recipient's email address
            name: The user's name for personalization
            verification_code: The verification code to send
            expiry_minutes: Minutes until the code expires
            code_type: Type of verification ('registration' or 'login')
            
        Returns:
            True if the email was sent successfully, False otherwise
        """
        try:
            if code_type == 'login':
                return self.email_service.send_login_code(
                    to_email=user_email,
                    name=name,
                    code=verification_code,
                    expiry_minutes=expiry_minutes
                )
            else:
                return self.email_service.send_registration_code(
                    to_email=user_email,
                    name=name,
                    code=verification_code,
                    expiry_minutes=expiry_minutes
                )
        except EmailError as e:
            logger.error(f"Failed to send verification code to {user_email}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending verification code: {e}")
            return False
    
    def send_welcome_email(self, user_email: str, name: str) -> bool:
        """
        Send a welcome email after successful registration.
        
        Args:
            user_email: The recipient's email address
            name: The user's name for personalization
            
        Returns:
            True if the email was sent successfully, False otherwise
        """
        try:
            return self.email_service.send_welcome_email(
                to_email=user_email,
                name=name
            )
        except EmailError as e:
            logger.error(f"Failed to send welcome email to {user_email}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending welcome email: {e}")
            return False
    
    # Keep static method for backward compatibility
    @staticmethod
    def send_verification_code_static(
        user_email: str,
        name: str,
        verification_code: str,
        expiry_minutes: int
    ) -> None:
        """
        Static method for backward compatibility.
        
        Deprecated: Use instance method send_verification_code instead.
        """
        service = NotificationService()
        service.send_verification_code(
            user_email=user_email,
            name=name,
            verification_code=verification_code,
            expiry_minutes=expiry_minutes,
            code_type='registration'
        )
