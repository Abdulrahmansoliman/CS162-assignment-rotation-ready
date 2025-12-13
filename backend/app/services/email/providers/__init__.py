"""
Email Providers Module

Contains implementations for different email providers.
"""

from app.services.email.providers.base import EmailProvider
from app.services.email.providers.flask_mail_provider import FlaskMailProvider
from app.services.email.providers.console_provider import ConsoleProvider

__all__ = [
    'EmailProvider',
    'FlaskMailProvider',
    'ConsoleProvider',
]
