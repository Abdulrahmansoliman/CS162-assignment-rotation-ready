"""
Email Templates Module

Contains HTML and text templates for transactional emails.
"""

from app.services.email.templates.template_engine import TemplateEngine
from app.services.email.templates.verification_templates import VerificationTemplates

__all__ = [
    'TemplateEngine',
    'VerificationTemplates',
]
