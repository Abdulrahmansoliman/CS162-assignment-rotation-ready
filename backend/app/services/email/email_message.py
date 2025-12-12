"""
Email Message Models

Data classes for representing email messages and recipients.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class EmailRecipient:
    """Represents an email recipient."""
    email: str
    name: Optional[str] = None
    
    def __str__(self) -> str:
        if self.name:
            return f"{self.name} <{self.email}>"
        return self.email
    
    @classmethod
    def from_string(cls, email_string: str) -> 'EmailRecipient':
        """Parse an email string like 'Name <email@example.com>' or 'email@example.com'."""
        email_string = email_string.strip()
        if '<' in email_string and '>' in email_string:
            name = email_string.split('<')[0].strip()
            email = email_string.split('<')[1].split('>')[0].strip()
            return cls(email=email, name=name if name else None)
        return cls(email=email_string)


@dataclass
class EmailMessage:
    """
    Represents an email message to be sent.
    
    Attributes:
        to: List of primary recipients
        subject: Email subject line
        body_text: Plain text body (optional if body_html provided)
        body_html: HTML body (optional if body_text provided)
        cc: List of CC recipients
        bcc: List of BCC recipients
        reply_to: Reply-to email address
        headers: Additional email headers
        attachments: List of attachment file paths
        template_name: Name of template to use (alternative to body_text/body_html)
        template_context: Context variables for template rendering
    """
    to: List[EmailRecipient]
    subject: str
    body_text: Optional[str] = None
    body_html: Optional[str] = None
    cc: List[EmailRecipient] = field(default_factory=list)
    bcc: List[EmailRecipient] = field(default_factory=list)
    reply_to: Optional[str] = None
    headers: Dict[str, str] = field(default_factory=dict)
    attachments: List[str] = field(default_factory=list)
    template_name: Optional[str] = None
    template_context: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate message after initialization."""
        if not self.to:
            raise ValueError("Email must have at least one recipient")
        
        # Convert string recipients to EmailRecipient objects
        self.to = [self._ensure_recipient(r) for r in self.to]
        self.cc = [self._ensure_recipient(r) for r in self.cc]
        self.bcc = [self._ensure_recipient(r) for r in self.bcc]
    
    @staticmethod
    def _ensure_recipient(recipient) -> EmailRecipient:
        """Convert string to EmailRecipient if necessary."""
        if isinstance(recipient, str):
            return EmailRecipient.from_string(recipient)
        return recipient
    
    @property
    def all_recipients(self) -> List[str]:
        """Get all recipient email addresses."""
        return [r.email for r in self.to + self.cc + self.bcc]
    
    @classmethod
    def simple(
        cls,
        to: str,
        subject: str,
        body_text: str,
        body_html: Optional[str] = None
    ) -> 'EmailMessage':
        """Create a simple email message with minimal configuration."""
        return cls(
            to=[EmailRecipient.from_string(to)],
            subject=subject,
            body_text=body_text,
            body_html=body_html
        )
