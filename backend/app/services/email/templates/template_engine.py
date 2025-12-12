"""
Template Engine

Simple template rendering engine for email templates.
Uses Python string formatting with fallback support.
"""

from typing import Dict, Any, Tuple, Optional
from app.services.email.exceptions import EmailTemplateError


class TemplateEngine:
    """
    Simple template engine for rendering email templates.
    
    Supports both HTML and plain text templates with variable substitution.
    """
    
    # Registry of available templates
    _templates: Dict[str, Dict[str, str]] = {}
    
    @classmethod
    def register(
        cls,
        name: str,
        text_template: str,
        html_template: Optional[str] = None
    ) -> None:
        """
        Register a new email template.
        
        Args:
            name: Unique template name
            text_template: Plain text template with {variable} placeholders
            html_template: Optional HTML template with {variable} placeholders
        """
        cls._templates[name] = {
            'text': text_template,
            'html': html_template,
        }
    
    @classmethod
    def render(
        cls,
        template_name: str,
        context: Dict[str, Any]
    ) -> Tuple[str, Optional[str]]:
        """
        Render a template with the given context.
        
        Args:
            template_name: Name of the registered template
            context: Dictionary of variables to substitute
            
        Returns:
            Tuple of (text_body, html_body)
            
        Raises:
            EmailTemplateError: If template not found or rendering fails
        """
        if template_name not in cls._templates:
            raise EmailTemplateError(f"Template '{template_name}' not found")
        
        template = cls._templates[template_name]
        
        try:
            text_body = template['text'].format(**context)
            html_body = None
            
            if template['html']:
                html_body = template['html'].format(**context)
            
            return text_body, html_body
            
        except KeyError as e:
            raise EmailTemplateError(
                f"Missing template variable: {e}",
                original_error=e
            )
        except Exception as e:
            raise EmailTemplateError(
                f"Failed to render template '{template_name}'",
                original_error=e
            )
    
    @classmethod
    def get_template_names(cls) -> list:
        """Get list of all registered template names."""
        return list(cls._templates.keys())
    
    @classmethod
    def has_template(cls, name: str) -> bool:
        """Check if a template is registered."""
        return name in cls._templates
