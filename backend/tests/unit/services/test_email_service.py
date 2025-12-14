"""
Unit Tests for Email Service Module

Tests for EmailMessage, EmailRecipient, TemplateEngine, and EmailService.
Focused on core functionality without external dependencies.
"""
import pytest

from app.services.email.email_message import EmailMessage, EmailRecipient
from app.services.email.templates.template_engine import TemplateEngine
from app.services.email.exceptions import (
    EmailTemplateError,
)


class TestEmailRecipient:
    """Tests for EmailRecipient data class."""
    
    def test_create_with_email_only(self):
        """Should create recipient with just email."""
        recipient = EmailRecipient(email="test@example.com")
        
        assert recipient.email == "test@example.com"
        assert recipient.name is None
        assert str(recipient) == "test@example.com"
    
    def test_create_with_name_and_email(self):
        """Should create recipient with name and email."""
        recipient = EmailRecipient(email="test@example.com", name="John Doe")
        
        assert recipient.email == "test@example.com"
        assert recipient.name == "John Doe"
        assert str(recipient) == "John Doe <test@example.com>"
    
    def test_from_string_simple_email(self):
        """Should parse simple email string."""
        recipient = EmailRecipient.from_string("test@example.com")
        
        assert recipient.email == "test@example.com"
        assert recipient.name is None
    
    def test_from_string_with_name(self):
        """Should parse 'Name <email>' format."""
        recipient = EmailRecipient.from_string("John Doe <john@example.com>")
        
        assert recipient.email == "john@example.com"
        assert recipient.name == "John Doe"


class TestEmailMessage:
    """Tests for EmailMessage data class."""
    
    def test_create_simple_message(self):
        """Should create a simple email message."""
        message = EmailMessage.simple(
            to="user@example.com",
            subject="Test Subject",
            body_text="Hello World"
        )
        
        assert len(message.to) == 1
        assert message.to[0].email == "user@example.com"
        assert message.subject == "Test Subject"
        assert message.body_text == "Hello World"
    
    def test_create_with_multiple_recipients(self):
        """Should handle multiple recipients."""
        message = EmailMessage(
            to=[
                EmailRecipient(email="user1@example.com"),
                EmailRecipient(email="user2@example.com"),
            ],
            subject="Test",
            body_text="Hello"
        )
        
        assert len(message.to) == 2
        assert message.all_recipients == ["user1@example.com", "user2@example.com"]
    
    def test_create_with_string_recipients(self):
        """Should auto-convert string recipients to EmailRecipient."""
        message = EmailMessage(
            to=["user@example.com"],
            subject="Test",
            body_text="Hello"
        )
        
        assert isinstance(message.to[0], EmailRecipient)
        assert message.to[0].email == "user@example.com"
    
    def test_raises_error_without_recipients(self):
        """Should raise error if no recipients provided."""
        with pytest.raises(ValueError, match="at least one recipient"):
            EmailMessage(to=[], subject="Test", body_text="Hello")
    
    def test_all_recipients_includes_cc_bcc(self):
        """Should include to, cc, and bcc in all_recipients."""
        message = EmailMessage(
            to=[EmailRecipient(email="to@example.com")],
            cc=[EmailRecipient(email="cc@example.com")],
            bcc=[EmailRecipient(email="bcc@example.com")],
            subject="Test",
            body_text="Hello"
        )
        
        assert set(message.all_recipients) == {
            "to@example.com",
            "cc@example.com", 
            "bcc@example.com"
        }


class TestTemplateEngine:
    """Tests for TemplateEngine with Jinja2 file-based templates."""
    
    def test_register_and_render_template(self):
        """Should register and render a template from files."""
        TemplateEngine.register(
            name="test_template",
            html_template="html/test.html",
            text_template="text/test.txt"
        )
        
        text, html = TemplateEngine.render("test_template", {"name": "World"})
        
        assert text == "Hello World!"
        assert html == "<h1>Hello World!</h1>"
    
    def test_render_text_only_template(self):
        """Should handle template with no HTML."""
        TemplateEngine.register(
            name="text_only",
            html_template=None,
            text_template="text/text_only.txt"
        )
        
        text, html = TemplateEngine.render("text_only", {"value": "123"})
        
        assert text == "Plain text: 123"
        assert html is None
    
    def test_render_missing_template_raises_error(self):
        """Should raise error for non-existent template."""
        with pytest.raises(EmailTemplateError, match="not found"):
            TemplateEngine.render("nonexistent_template", {})
    
    def test_render_missing_variable_renders_empty(self):
        """Jinja2 renders missing variables as empty by default."""
        TemplateEngine.register(
            name="needs_var",
            html_template=None,
            text_template="text/needs_var.txt"
        )
        
        # Jinja2 silently renders missing variables as empty
        text, html = TemplateEngine.render("needs_var", {"name": "John"})  # missing 'code'
        assert "John" in text
        # Template says "code is {{ code }}" - missing code renders as empty string
        assert text == "Hello John, code is"
    
    def test_has_template(self):
        """Should check if template exists."""
        TemplateEngine.register(
            name="exists",
            html_template="html/test.html",
            text_template="text/test.txt"
        )
        
        assert TemplateEngine.has_template("exists") is True
        assert TemplateEngine.has_template("does_not_exist") is False


class TestConsoleProvider:
    """Tests for ConsoleProvider (development email backend)."""
    
    def test_is_always_configured(self):
        """Console provider should always be configured."""
        from app.services.email.providers.console_provider import ConsoleProvider
        
        provider = ConsoleProvider()
        
        assert provider.is_configured() is True
        assert provider.name == "Console (Development)"
    
    def test_send_returns_true(self, capsys):
        """Should print email and return True."""
        from app.services.email.providers.console_provider import ConsoleProvider
        
        provider = ConsoleProvider()
        message = EmailMessage.simple(
            to="test@example.com",
            subject="Test Subject",
            body_text="Test Body"
        )
        
        result = provider.send(message, "sender@example.com", "Sender Name")
        
        assert result is True
        
        # Check console output contains key info
        captured = capsys.readouterr()
        assert "test@example.com" in captured.out
        assert "Test Subject" in captured.out
        assert "Test Body" in captured.out


class TestEmailServiceWithMockedProvider:
    """Tests for EmailService with mocked provider."""
    
    @pytest.fixture(autouse=True)
    def reset_singleton(self):
        """Reset EmailService singleton between tests."""
        from app.services.email.email_service import EmailService
        EmailService.reset()
        yield
        EmailService.reset()
    
    def test_send_registration_code(self, app_context):
        """Should send registration verification email."""
        from app.services.email.email_service import EmailService
        from app.services.email.providers.console_provider import ConsoleProvider
        
        # Use console provider (no real SMTP)
        mock_provider = ConsoleProvider()
        service = EmailService(provider=mock_provider)
        
        result = service.send_registration_code(
            to_email="user@example.com",
            name="John",
            code="ABC123",
            expiry_minutes=15
        )
        
        assert result is True
    
    def test_send_login_code(self, app_context):
        """Should send login verification email."""
        from app.services.email.email_service import EmailService
        from app.services.email.providers.console_provider import ConsoleProvider
        
        mock_provider = ConsoleProvider()
        service = EmailService(provider=mock_provider)
        
        result = service.send_login_code(
            to_email="user@example.com",
            name="Jane",
            code="XYZ789",
            expiry_minutes=10
        )
        
        assert result is True
    
    def test_send_simple_email(self, app_context):
        """Should send a simple email without template."""
        from app.services.email.email_service import EmailService
        from app.services.email.providers.console_provider import ConsoleProvider
        
        mock_provider = ConsoleProvider()
        service = EmailService(provider=mock_provider)
        
        result = service.send_simple(
            to="user@example.com",
            subject="Hello",
            body="Welcome to the app!"
        )
        
        assert result is True


class TestNotificationServiceIntegration:
    """Tests for NotificationService using EmailService (async/fire-and-forget)."""
    
    def test_send_verification_code_registration(self, app_context):
        """Should send registration code via EmailService (async - no return value)."""
        from app.services.auth.notification_service import NotificationService
        from app.services.email.email_service import EmailService
        from app.services.email.providers.console_provider import ConsoleProvider
        
        # Reset and inject console provider
        EmailService.reset()
        email_service = EmailService(provider=ConsoleProvider())
        
        notification_service = NotificationService(email_service=email_service)
        
        # Async methods return None (fire-and-forget)
        result = notification_service.send_verification_code(
            user_email="test@example.com",
            name="Test User",
            verification_code="123456",
            expiry_minutes=15,
            code_type='registration'
        )
        
        assert result is None  # Async fire-and-forget returns None
    
    def test_send_verification_code_login(self, app_context):
        """Should send login code via EmailService (async - no return value)."""
        from app.services.auth.notification_service import NotificationService
        from app.services.email.email_service import EmailService
        from app.services.email.providers.console_provider import ConsoleProvider
        
        EmailService.reset()
        email_service = EmailService(provider=ConsoleProvider())
        
        notification_service = NotificationService(email_service=email_service)
        
        # Async methods return None (fire-and-forget)
        result = notification_service.send_verification_code(
            user_email="test@example.com",
            name="Test User",
            verification_code="ABCDEF",
            expiry_minutes=15,
            code_type='login'
        )
        
        assert result is None  # Async fire-and-forget returns None
