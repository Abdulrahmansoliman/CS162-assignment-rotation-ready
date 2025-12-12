"""
Email Service Module

A modular, provider-agnostic email service for sending transactional emails.
Supports multiple providers and HTML templates.
"""

from app.services.email.email_service import EmailService
from app.services.email.email_message import EmailMessage, EmailRecipient
from app.services.email.exceptions import (
    EmailError,
    EmailConfigurationError,
    EmailDeliveryError,
    EmailTemplateError,
)

__all__ = [
    'EmailService',
    'EmailMessage',
    'EmailRecipient',
    'EmailError',
    'EmailConfigurationError',
    'EmailDeliveryError',
    'EmailTemplateError',
]
