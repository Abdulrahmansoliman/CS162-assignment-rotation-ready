"""
Flask-Mail Provider

Email provider implementation using Flask-Mail for SMTP delivery.
"""

from typing import Optional
from flask import current_app
from flask_mail import Mail, Message

from app.services.email.providers.base import EmailProvider
from app.services.email.email_message import EmailMessage
from app.services.email.exceptions import EmailDeliveryError, EmailConfigurationError


class FlaskMailProvider(EmailProvider):
    """
    Email provider using Flask-Mail for SMTP delivery.
    
    Requires Flask-Mail to be initialized in the Flask application.
    """
    
    def __init__(self, mail: Mail = None):
        """
        Initialize the Flask-Mail provider.
        
        Args:
            mail: Optional Flask-Mail instance. If not provided,
                  will attempt to get from current_app extensions.
        """
        self._mail = mail
    
    @property
    def mail(self) -> Mail:
        """Get the Flask-Mail instance."""
        if self._mail:
            return self._mail
        
        # Try to get from current app extensions
        if current_app and hasattr(current_app, 'extensions'):
            mail = current_app.extensions.get('mail')
            if mail:
                return mail
        
        raise EmailConfigurationError(
            "Flask-Mail is not initialized. "
            "Ensure mail.init_app(app) is called in the application factory."
        )
    
    @property
    def name(self) -> str:
        return "Flask-Mail (SMTP)"
    
    def is_configured(self) -> bool:
        """Check if Flask-Mail is properly configured."""
        try:
            config = current_app.config
            # Check required configuration
            return bool(
                config.get('MAIL_SERVER') and
                config.get('MAIL_PORT')
            )
        except RuntimeError:
            # No application context
            return False
    
    def send(
        self,
        message: EmailMessage,
        sender: str,
        sender_name: Optional[str] = None
    ) -> bool:
        """
        Send an email using Flask-Mail.
        
        Args:
            message: The EmailMessage to send
            sender: The sender email address
            sender_name: Optional sender display name
            
        Returns:
            True if the email was sent successfully
            
        Raises:
            EmailDeliveryError: If the email could not be sent
        """
        try:
            # Build sender string
            if sender_name:
                sender_string = f"{sender_name} <{sender}>"
            else:
                sender_string = sender
            
            # Create Flask-Mail Message
            msg = Message(
                subject=message.subject,
                sender=sender_string,
                recipients=[str(r) for r in message.to],
                cc=[str(r) for r in message.cc] if message.cc else None,
                bcc=[str(r) for r in message.bcc] if message.bcc else None,
                body=message.body_text,
                html=message.body_html,
                reply_to=message.reply_to,
                extra_headers=message.headers if message.headers else None,
            )
            
            # Send the email
            self.mail.send(msg)
            
            return True
            
        except EmailConfigurationError:
            raise
        except Exception as e:
            raise EmailDeliveryError(
                f"Failed to send email via Flask-Mail",
                original_error=e
            )
