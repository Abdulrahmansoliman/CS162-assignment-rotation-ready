"""
Email Provider Interface

Abstract base class for email providers.
Enables swapping between different email backends (SMTP, SendGrid, etc.)
"""

from abc import ABC, abstractmethod
from typing import Optional
from app.services.email.email_message import EmailMessage


class EmailProvider(ABC):
    """
    Abstract base class for email providers.
    
    Implement this interface to add support for different email backends.
    """
    
    @abstractmethod
    def send(self, message: EmailMessage, sender: str, sender_name: Optional[str] = None) -> bool:
        """
        Send an email message.
        
        Args:
            message: The EmailMessage to send
            sender: The sender email address
            sender_name: Optional sender display name
            
        Returns:
            True if the email was sent successfully
            
        Raises:
            EmailDeliveryError: If the email could not be sent
        """
        pass
    
    @abstractmethod
    def is_configured(self) -> bool:
        """
        Check if the provider is properly configured.
        
        Returns:
            True if the provider can send emails
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the provider name for logging purposes."""
        pass
