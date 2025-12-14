"""
Email Service

Main email service that orchestrates providers and templates.
Provides a clean API for sending transactional emails.
Supports async (fire-and-forget) sending for non-blocking operations.
"""

import logging
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, List, Callable

from flask import current_app, Flask

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


# Thread pool for async email sending (module-level, shared across instances)
# Using max_workers=3 to limit concurrent SMTP connections
_executor: Optional[ThreadPoolExecutor] = None
_executor_lock = threading.Lock()

# Instance lock for EmailService (singleton)
_instance_lock = threading.Lock()


def _get_executor() -> ThreadPoolExecutor:
    """Get or create the thread pool executor (thread-safe)."""
    global _executor
    if _executor is None:
        with _executor_lock:
            # Double-check locking pattern
            if _executor is None:
                _executor = ThreadPoolExecutor(
                    max_workers=3,
                    thread_name_prefix="email_worker"
                )
    return _executor


class EmailService:
    """
    Main email service for sending transactional emails.
    
    Features:
    - Provider-agnostic: Swap between SMTP, console, or other providers
    - Template support: Use pre-defined or custom templates
    - Graceful degradation: Falls back to console in development
    - Configuration-based: Respects MAIL_ENABLED flag
    - Async support: Fire-and-forget sending with send_async()
    
    Usage:
        email_service = EmailService()
        
        # Send a simple email (blocking)
        email_service.send_simple(
            to="user@example.com",
            subject="Hello",
            body="Welcome!"
        )
        
        # Send async (non-blocking, fire-and-forget)
        email_service.send_async(message)
        
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
        with _instance_lock:
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
        self._app: Optional[Flask] = None  # Cached app reference for async
        self._register_templates()
        self._initialized = True 
    
    @classmethod
    def reset(cls) -> None:
        """Reset the singleton instance. Useful for testing."""
        with _instance_lock:
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
    
    def _get_app(self) -> Flask:
        """
        Get the Flask app instance (thread-safe).
        
        Caches the app reference for use in background threads
        where current_app is not available.
        """
        if self._app is None:
            try:
                self._app = current_app._get_current_object()
            except RuntimeError:
                raise EmailError("No Flask application context available for async send")
        return self._app
    
    def _send_in_thread(
        self,
        message: EmailMessage,
        app: Flask,
        sender: str,
        sender_name: str,
        on_error: Optional[Callable[[Exception], None]] = None
    ) -> None:
        """
        Send email in a background thread with proper Flask context.
        
        Args:
            message: The prepared EmailMessage (template already rendered)
            app: Flask app instance for context
            sender: Sender email address
            sender_name: Sender display name
            on_error: Optional callback for error handling
        """
        try:
            with app.app_context():
                result = self.provider.send(
                    message=message,
                    sender=sender,
                    sender_name=sender_name
                )
                
                if result:
                    logger.info(
                        f"[Async] Email sent successfully via {self.provider.name} "
                        f"to {message.all_recipients}"
                    )
                else:
                    logger.warning(
                        f"[Async] Email sending returned False for {message.all_recipients}"
                    )
                    
        except Exception as e:
            logger.error(f"[Async] Failed to send email: {e}")
            if on_error:
                try:
                    on_error(e)
                except Exception as callback_error:
                    logger.error(f"[Async] Error callback failed: {callback_error}")
    
    def send_async(
        self,
        message: EmailMessage,
        on_error: Optional[Callable[[Exception], None]] = None
    ) -> None:
        """
        Send an email asynchronously (fire-and-forget).
        
        The email is sent in a background thread, so this method returns
        immediately. Use this for non-critical emails where you don't need
        to wait for delivery confirmation.
        
        Args:
            message: The EmailMessage to send
            on_error: Optional callback function called if sending fails.
                     Receives the exception as argument.
        
        Note:
            - Must be called within Flask application context
            - Template rendering happens synchronously before dispatch
            - Errors are logged but not raised (fire-and-forget)
        
        Example:
            email_service.send_async(message)  # Returns immediately
            
            # With error callback
            email_service.send_async(
                message,
                on_error=lambda e: log_to_monitoring(e)
            )
        """
        # Render template synchronously (needs current context for config)
        if message.template_name:
            text_body, html_body = TemplateEngine.render(
                message.template_name,
                message.template_context
            )
            message.body_text = text_body
            message.body_html = html_body
        
        # Capture app, sender info while we have context
        app = self._get_app()
        sender = self.sender
        sender_name = self.sender_name
        
        # Dispatch to thread pool
        executor = _get_executor()
        executor.submit(
            self._send_in_thread,
            message,
            app,
            sender,
            sender_name,
            on_error
        )
        
        logger.debug(f"[Async] Email queued for {message.all_recipients}")

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
    
    def _build_registration_code_message(
        self, to_email: str, name: str, code: str, expiry_minutes: int
    ) -> EmailMessage:
        """Build a registration verification code email message."""
        return EmailMessage(
            to=[EmailRecipient.from_string(to_email)],
            subject="Verify your Rotation Ready account",
            template_name=VerificationTemplates.REGISTRATION_CODE,
            template_context={
                'name': name,
                'code': code,
                'expiry_minutes': expiry_minutes
            }
        )
    
    def _build_login_code_message(
        self, to_email: str, name: str, code: str, expiry_minutes: int
    ) -> EmailMessage:
        """Build a login verification code email message."""
        return EmailMessage(
            to=[EmailRecipient.from_string(to_email)],
            subject="Your Rotation Ready login code",
            template_name=VerificationTemplates.LOGIN_CODE,
            template_context={
                'name': name,
                'code': code,
                'expiry_minutes': expiry_minutes
            }
        )
    
    def _build_welcome_message(self, to_email: str, name: str) -> EmailMessage:
        """Build a welcome email message."""
        return EmailMessage(
            to=[EmailRecipient.from_string(to_email)],
            subject="Welcome to Rotation Ready! 🎉",
            template_name=VerificationTemplates.WELCOME,
            template_context={'name': name}
        )
    
    def send_registration_code_async(
        self, to_email: str, name: str, code: str, expiry_minutes: int,
        on_error: Optional[Callable[[Exception], None]] = None
    ) -> None:
        """Send a registration verification code email asynchronously."""
        self.send_async(
            self._build_registration_code_message(to_email, name, code, expiry_minutes),
            on_error=on_error
        )
    
    def send_login_code_async(
        self, to_email: str, name: str, code: str, expiry_minutes: int,
        on_error: Optional[Callable[[Exception], None]] = None
    ) -> None:
        """Send a login verification code email asynchronously."""
        self.send_async(
            self._build_login_code_message(to_email, name, code, expiry_minutes),
            on_error=on_error
        )
    
    def send_welcome_email_async(
        self, to_email: str, name: str,
        on_error: Optional[Callable[[Exception], None]] = None
    ) -> None:
        """Send a welcome email asynchronously."""
        self.send_async(self._build_welcome_message(to_email, name), on_error=on_error)


# Convenience function for getting the email service instance
def get_email_service() -> EmailService:
    """Get the EmailService singleton instance."""
    return EmailService()
