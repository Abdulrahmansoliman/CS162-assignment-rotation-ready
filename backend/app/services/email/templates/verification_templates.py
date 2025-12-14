"""
Verification Email Templates

Registers verification-related email templates with the TemplateEngine.
Templates are stored as Jinja2 files in the jinja/ folder.
"""

from app.services.email.templates.template_engine import TemplateEngine


class VerificationTemplates:
    """
    Pre-defined templates for verification emails.
    
    Call register_all() to register these templates with the TemplateEngine.
    
    Template structure:
    - jinja/html/base.html - Shared layout (header, footer, styling)
    - jinja/html/*.html - Email-specific HTML templates
    - jinja/html/components/*.html - Reusable components
    - jinja/text/*.txt - Plain text versions
    """
    
    # Template Names
    REGISTRATION_CODE = 'verification_registration'
    LOGIN_CODE = 'verification_login'
    WELCOME = 'welcome'
    
    @classmethod
    def register_all(cls) -> None:
        """Register all verification templates."""
        # Registration email - primary theme (red)
        TemplateEngine.register(
            name=cls.REGISTRATION_CODE,
            html_template='html/registration.html',
            text_template='text/registration.txt',
            theme='primary'
        )
        
        # Login email - success theme (green)
        TemplateEngine.register(
            name=cls.LOGIN_CODE,
            html_template='html/login.html',
            text_template='text/login.txt',
            theme='success'
        )
        
        # Welcome email - primary theme (red)
        TemplateEngine.register(
            name=cls.WELCOME,
            html_template='html/welcome.html',
            text_template='text/welcome.txt',
            theme='primary'
        )
