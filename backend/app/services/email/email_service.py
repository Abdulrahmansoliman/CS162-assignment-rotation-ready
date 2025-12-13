"""
Email Service

Main email service that orchestrates providers and templates.
Provides a clean API for sending transactional emails.
"""

import logging
from typing import Optional, List

from flask import current_app

from app.services.email.email_message import EmailMessage, EmailRecipient
from app.services.email.providers.base import EmailProvider
from app.services.email.providers.flask_mail_provider import FlaskMailProvider
from app.services.email.providers.console_provider import ConsoleProvider
from app.services.email.templates.template_engine import TemplateEngine
from app.services.email.templates.verification_templates import VerificationTemplates
from app.services.email.exceptions import (
    EmailError,
    EmailDeliveryError,
)


logger = logging.getLogger(__name__)


class EmailService:
    """
    Main email service for sending transactional emails.
    
    Features:
    - Provider-agnostic: Swap between SMTP, console, or other providers
    - Template support: Use pre-defined or custom templates
    - Graceful degradation: Falls back to console in development
    - Configuration-based: Respects MAIL_ENABLED flag
    
    Usage:
        email_service = EmailService()
        
        # Send a simple email
        email_service.send_simple(
            to="user@example.com",
            subject="Hello",
            body="Welcome!"
        )
        
        # Send using a template
        email_service.send_verification_code(
            to_email="user@example.com",
            name="John",
            code="ABC123",
            expiry_minutes=15
        )
    """
    
    _instance: Optional['EmailService'] = None
    
    def __new__(cls, *args, **kwargs):
        """Singleton pattern for EmailService."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, provider: Optional[EmailProvider] = None):
        """
        Initialize the email service.
        
        Args:
            provider: Optional email provider. If not provided, will auto-select
                     based on configuration.
        
        Note:
            Uses instance variable _initialized to track initialization state.
            This ensures proper reset behavior when testing with different providers.
        """
        # Check instance variable, not class variable, for thread safety
        if getattr(self, '_initialized', False):
            return
        
        self._provider = provider
        self._register_templates()
        self._initialized = True 
    
    @classmethod
    def reset(cls) -> None:
        """Reset the singleton instance. Useful for testing."""
        cls._instance = None
    
    def _register_templates(self) -> None:
        """Register all email templates."""
        VerificationTemplates.register_all()
    
    @property
    def provider(self) -> EmailProvider:
        """
        Get the configured email provider.
        
        Auto-selects based on configuration:
        - If MAIL_ENABLED is False: ConsoleProvider
        - If MAIL_ENABLED is True: FlaskMailProvider
        """
        if self._provider:
            return self._provider
        
        try:
            config = current_app.config
            mail_enabled = config.get('MAIL_ENABLED', False)
            
            if mail_enabled:
                provider = FlaskMailProvider()
                if provider.is_configured():
                    self._provider = provider
                else:
                    logger.warning(
                        "MAIL_ENABLED is True but Flask-Mail is not properly configured. "
                        "Falling back to ConsoleProvider."
                    )
                    self._provider = ConsoleProvider()
            else:
                self._provider = ConsoleProvider()
            
            return self._provider
                
        except RuntimeError:
            # No application context
            self._provider = ConsoleProvider()
            logger.warning(
                "No Flask application context. Falling back to ConsoleProvider."
            )
            return self._provider
    
    @property
    def sender(self) -> str:
        """Get the default sender email address."""
        try:
            return current_app.config.get(
                'MAIL_DEFAULT_SENDER',
                'noreply@rotationready.com'
            )
        except RuntimeError:
            return 'noreply@rotationready.com'
    
    @property
    def sender_name(self) -> str:
        """Get the default sender display name."""
        try:
            return current_app.config.get(
                'MAIL_DEFAULT_SENDER_NAME',
                'Rotation Ready'
            )
        except RuntimeError:
            return 'Rotation Ready'
    
    def send(self, message: EmailMessage) -> bool:
        """
        Send an email message.
        
        Args:
            message: The EmailMessage to send
            
        Returns:
            True if the email was sent successfully
            
        Raises:
            EmailDeliveryError: If sending fails and suppress_errors is False
        """
        try:
            # Render template if specified
            if message.template_name:
                text_body, html_body = TemplateEngine.render(
                    message.template_name,
                    message.template_context
                )
                message.body_text = text_body
                message.body_html = html_body
            
            # Send via provider
            result = self.provider.send(
                message=message,
                sender=self.sender,
                sender_name=self.sender_name
            )
            
            if result:
                logger.info(
                    f"Email sent successfully via {self.provider.name} "
                    f"to {message.all_recipients}"
                )
            
            return result
            
        except EmailError:
            raise
        except Exception as e:
            raise EmailDeliveryError(
                "Unexpected error sending email",
                original_error=e
            )
    
    def send_simple(
        self,
        to: str,
        subject: str,
        body: str,
        html_body: Optional[str] = None
    ) -> bool:
        """
        Send a simple email without templates.
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Plain text body
            html_body: Optional HTML body
            
        Returns:
            True if sent successfully
        """
        message = EmailMessage.simple(
            to=to,
            subject=subject,
            body_text=body,
            body_html=html_body
        )
        return self.send(message)
    
    def send_with_template(
        self,
        to: str,
        subject: str,
        template_name: str,
        context: dict,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None
    ) -> bool:
        """
        Send an email using a template.
        
        Args:
            to: Recipient email address
            subject: Email subject
            template_name: Name of the registered template
            context: Template context variables
            cc: Optional CC recipients
            bcc: Optional BCC recipients
            
        Returns:
            True if sent successfully
        """
        message = EmailMessage(
            to=[EmailRecipient.from_string(to)],
            subject=subject,
            template_name=template_name,
            template_context=context,
            cc=[EmailRecipient.from_string(e) for e in (cc or [])],
            bcc=[EmailRecipient.from_string(e) for e in (bcc or [])]
        )
        return self.send(message)
    
    # Convenience methods for common email types
    
    def send_registration_code(
        self,
        to_email: str,
        name: str,
        code: str,
        expiry_minutes: int
    ) -> bool:
        """
        Send a registration verification code email.
        
        Args:
            to_email: Recipient email address
            name: User's name for personalization
            code: The verification code
            expiry_minutes: Minutes until code expires
            
        Returns:
            True if sent successfully
        """
        return self.send_with_template(
            to=to_email,
            subject="Verify your Rotation Ready account",
            template_name=VerificationTemplates.REGISTRATION_CODE,
            context={
                'name': name,
                'code': code,
                'expiry_minutes': expiry_minutes
            }
        )
    
    def send_login_code(
        self,
        to_email: str,
        name: str,
        code: str,
        expiry_minutes: int
    ) -> bool:
        """
        Send a login verification code email.
        
        Args:
            to_email: Recipient email address
            name: User's name for personalization
            code: The verification code
            expiry_minutes: Minutes until code expires
            
        Returns:
            True if sent successfully
        """
        return self.send_with_template(
            to=to_email,
            subject="Your Rotation Ready login code",
            template_name=VerificationTemplates.LOGIN_CODE,
            context={
                'name': name,
                'code': code,
                'expiry_minutes': expiry_minutes
            }
        )
    
    def send_welcome_email(self, to_email: str, name: str) -> bool:
        """
        Send a welcome email after successful registration.
        
        Args:
            to_email: Recipient email address
            name: User's name for personalization
            
        Returns:
            True if sent successfully
        """
        return self.send_with_template(
            to=to_email,
            subject="Welcome to Rotation Ready! 🎉",
            template_name=VerificationTemplates.WELCOME,
            context={'name': name}
        )


# Convenience function for getting the email service instance
def get_email_service() -> EmailService:
    """Get the EmailService singleton instance."""
    return EmailService()
