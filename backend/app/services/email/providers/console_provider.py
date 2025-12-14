"""
Console Provider

Development/testing email provider that logs emails to console.
Useful for local development without SMTP configuration.
"""

from typing import Optional
import logging

from app.services.email.providers.base import EmailProvider
from app.services.email.email_message import EmailMessage


logger = logging.getLogger(__name__)


class ConsoleProvider(EmailProvider):
    """
    Email provider that outputs emails to console/logs.
    
    Useful for development and testing environments.
    """
    
    def __init__(self, log_level: int = logging.INFO):
        """
        Initialize the console provider.
        
        Args:
            log_level: Logging level for email output
        """
        self.log_level = log_level
    
    @property
    def name(self) -> str:
        return "Console (Development)"
    
    def is_configured(self) -> bool:
        """Console provider is always configured."""
        return True
    
    def send(
        self,
        message: EmailMessage,
        sender: str,
        sender_name: Optional[str] = None
    ) -> bool:
        """
        Log the email to console instead of sending.
        
        Args:
            message: The EmailMessage to log
            sender: The sender email address
            sender_name: Optional sender display name
            
        Returns:
            True always (console logging doesn't fail)
        """
        sender_display = f"{sender_name} <{sender}>" if sender_name else sender
        cc_line = f"\nCC:      {', '.join(str(r) for r in message.cc)}" if message.cc else ""
        bcc_line = f"\nBCC:     {', '.join(str(r) for r in message.bcc)}" if message.bcc else ""

        separator = "=" * 60
        email_output = f"""
{separator}
📧 EMAIL (Console Provider - Not Actually Sent)
{separator}
From:    {sender_display}
To:      {', '.join(str(r) for r in message.to)}{cc_line}{bcc_line}

Subject: {message.subject}
{separator}

{message.body_text or '[No plain text body]'}

{separator}
"""
        
        logger.log(self.log_level, email_output)
        
        # Also print to console for development visibility
        print(email_output)
        
        return True
