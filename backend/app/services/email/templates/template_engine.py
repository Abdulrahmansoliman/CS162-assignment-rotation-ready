"""
Template Engine

Jinja2-based template rendering engine for email templates.
Supports template inheritance and component includes.
"""

from pathlib import Path
from typing import Dict, Any, Tuple, Optional
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from app.services.email.exceptions import EmailTemplateError


# Base path for Jinja templates
TEMPLATES_DIR = Path(__file__).parent / 'jinja'


# Theme presets for email templates
THEMES = {
    'primary': {
        'header_color_start': '#cc0000',
        'header_color_end': '#ff4444',
        'accent_color': '#cc0000',
        'code_bg_color': '#f8f8f8',
    },
    'success': {
        'header_color_start': '#1d9a5c',
        'header_color_end': '#2fb872',
        'accent_color': '#1d9a5c',
        'code_bg_color': '#f0fdf4',
    },
}


class TemplateEngine:
    """
    Jinja2-based template engine for rendering email templates.
    
    Supports both HTML and plain text templates with:
    - Template inheritance ({% extends %})
    - Component includes ({% include %})
    - Variable substitution ({{ variable }})
    """
    
    # Jinja2 environment
    _env: Optional[Environment] = None
    
    # Registry of template configurations
    _templates: Dict[str, Dict[str, Any]] = {}
    
    @classmethod
    def _get_env(cls) -> Environment:
        """Get or create the Jinja2 environment."""
        if cls._env is None:
            cls._env = Environment(
                loader=FileSystemLoader(str(TEMPLATES_DIR)),
                autoescape=True
            )
        return cls._env
    
    @classmethod
    def register(
        cls,
        name: str,
        html_template: str,
        text_template: str,
        theme: str = 'primary'
    ) -> None:
        """
        Register a template configuration and proactively load templates.
        
        Templates are loaded and compiled at registration time (app startup),
        not on first render, eliminating any delay on first email send.
        
        Args:
            name: Unique template name
            html_template: Path to HTML template (relative to jinja folder)
            text_template: Path to text template (relative to jinja folder)
            theme: Color theme ('primary' or 'success')
        """
        env = cls._get_env()
        
        # Proactively load and compile templates NOW (at registration/startup)
        try:
            text_compiled = env.get_template(text_template)
            html_compiled = env.get_template(html_template)
        except TemplateNotFound as e:
            raise EmailTemplateError(f"Template file not found: {e}", original_error=e)
        
        cls._templates[name] = {
            'html': html_template,
            'text': text_template,
            'theme': theme,
            # Pre-loaded template objects - ready to render immediately
            '_text': text_compiled,
            '_html': html_compiled,
        }
    
    @classmethod
    def render(
        cls,
        template_name: str,
        context: Dict[str, Any]
    ) -> Tuple[str, Optional[str]]:
        """
        Render a template with the given context.
        
        Uses pre-loaded templates for instant rendering (no file I/O).
        
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
        
        config = cls._templates[template_name]
        
        # Merge theme variables into context
        theme_vars = THEMES.get(config['theme'], THEMES['primary'])
        full_context = {**theme_vars, **context}
        
        try:
            # Use pre-loaded templates (no file I/O, instant render)
            text_body = config['_text'].render(**full_context)
            
            html_body = None
            if config['_html']:
                html_body = config['_html'].render(**full_context)
            
            return text_body.strip(), html_body.strip() if html_body else None
            
        except Exception as e:
            raise EmailTemplateError(
                f"Failed to render template '{template_name}': {e}",
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
    
    @classmethod
    def clear(cls) -> None:
        """Clear all registered templates and reset environment."""
        cls._templates.clear()
        cls._env = None
