"""
Unit Tests for PasswordResetService

Tests password reset business logic with mocked dependencies.
Focuses on service logic without database interactions.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from app.services.auth.password_reset_service import (
    PasswordResetService,
    InvalidOrExpiredTokenError
)
from app.models.verification_code import VerificationCodeType
from app.models.user import User


@pytest.mark.unit
@pytest.mark.service
class TestPasswordResetServiceUnit:
    """Unit tests for PasswordResetService with mocked dependencies."""

    @pytest.fixture
    def mock_user_repo(self):
        """Mock UserRepository."""
        return Mock()

    @pytest.fixture
    def mock_verification_repo(self):
        """Mock VerificationCodeRepository."""
        return Mock()

    @pytest.fixture
    def mock_notification_service(self):
        """Mock NotificationService."""
        return Mock()

    @pytest.fixture
    def service(self, mock_user_repo, mock_verification_repo, mock_notification_service):
        """Create PasswordResetService with mocked dependencies."""
        return PasswordResetService(
            user_repository=mock_user_repo,
            verification_code_repository=mock_verification_repo,
            notification_service=mock_notification_service
        )

    @pytest.fixture
    def mock_user(self):
        """Create a mock user."""
        user = Mock(spec=User)
        user.user_id = 1
        user.email = 'test@example.com'
        user.first_name = 'John'
        return user

    # ============================================================================
    # Tests for request_reset()
    # ============================================================================

    @patch('app.services.auth.password_reset_service.secrets.token_urlsafe')
    def test_request_reset_creates_token_and_sends_email(
        self,
        mock_token,
        service,
        mock_user_repo,
        mock_verification_repo,
        mock_notification_service,
        mock_user,
        app_context
    ):
        """Test that request_reset creates token and sends email for valid user."""
        mock_token.return_value = 'test_token_12345'
        mock_user_repo.get_user_by_email.return_value = mock_user
        
        service.request_reset('test@example.com')
        
        # Verify user was looked up
        mock_user_repo.get_user_by_email.assert_called_once_with('test@example.com')
        
        # Verify old codes were invalidated
        mock_verification_repo.invalidate_user_codes.assert_called_once_with(
            user_id=1,
            code_type=VerificationCodeType.PASSWORD_RESET.code
        )
        
        # Verify new code was created
        mock_verification_repo.create_password_reset.assert_called_once()
        
        # Verify email was sent
        mock_notification_service.send_password_reset_email.assert_called_once()

    def test_request_reset_silently_succeeds_for_nonexistent_email(
        self,
        service,
        mock_user_repo,
        mock_verification_repo,
        mock_notification_service
    ):
        """Test that request_reset returns silently for non-existent email (prevent enumeration)."""
        mock_user_repo.get_user_by_email.return_value = None
        
        # Should not raise any exception
        service.request_reset('nonexistent@example.com')
        
        # Verify user was looked up
        mock_user_repo.get_user_by_email.assert_called_once_with('nonexistent@example.com')
        
        # Verify no code was created
        mock_verification_repo.create_password_reset.assert_not_called()
        
        # Verify no email was sent
        mock_notification_service.send_password_reset_email.assert_not_called()

    @patch('app.services.auth.password_reset_service.secrets.token_urlsafe')
    def test_request_reset_invalidates_old_codes(
        self,
        mock_token,
        service,
        mock_user_repo,
        mock_verification_repo,
        mock_user,
        app_context
    ):
        """Test that old password reset codes are invalidated before creating new one."""
        mock_token.return_value = 'new_token'
        mock_user_repo.get_user_by_email.return_value = mock_user
        
        service.request_reset('test@example.com')
        
        # Verify invalidation happened before creation
        assert mock_verification_repo.invalidate_user_codes.called
        assert mock_verification_repo.create_password_reset.called

    # ============================================================================
    # Tests for confirm_reset()
    # ============================================================================

    def test_confirm_reset_updates_password_with_valid_token(
        self,
        service,
        mock_user_repo,
        mock_verification_repo,
        app_context
    ):
        """Test that confirm_reset updates password when token is valid."""
        mock_code = Mock()
        mock_code.user_id = 1
        mock_code.verification_code_id = 123
        mock_code.code_hash = 'expected_hash'
        
        with patch.object(service, '_find_valid_reset_code', return_value=mock_code):
            service.confirm_reset('valid_token', 'newpassword123')
        
        # Verify password was updated
        mock_user_repo.update_password.assert_called_once_with(
            user_id=1,
            new_password='newpassword123'
        )
        
        # Verify code was marked as used
        mock_verification_repo.mark_as_used.assert_called_once_with(123)

    def test_confirm_reset_raises_error_for_invalid_token(
        self,
        service,
        app_context
    ):
        """Test that confirm_reset raises error for invalid token."""
        with patch.object(service, '_find_valid_reset_code', return_value=None):
            with pytest.raises(InvalidOrExpiredTokenError, match="Invalid or expired reset token"):
                service.confirm_reset('invalid_token', 'newpassword123')

    def test_confirm_reset_marks_code_as_used(
        self,
        service,
        mock_verification_repo,
        app_context
    ):
        """Test that confirm_reset marks the verification code as used."""
        mock_code = Mock()
        mock_code.user_id = 1
        mock_code.verification_code_id = 456
        
        with patch.object(service, '_find_valid_reset_code', return_value=mock_code):
            service.confirm_reset('valid_token', 'newpassword123')
        
        mock_verification_repo.mark_as_used.assert_called_once_with(456)

    # ============================================================================
    # Tests for _hash_token()
    # ============================================================================

    def test_hash_token_generates_salt_and_hash(
        self,
        service,
        app_context
    ):
        """Test that _hash_token generates salt and hash correctly."""
        token_hash, salt = service._hash_token('test_token')
        
        assert token_hash is not None
        assert salt is not None
        assert len(token_hash) == 64  # SHA256 hex length
        assert len(salt) == 32  # 16 bytes in hex

    def test_hash_token_produces_different_hashes_for_same_token(
        self,
        service,
        app_context
    ):
        """Test that same token produces different hashes due to different salts."""
        hash1, salt1 = service._hash_token('same_token')
        hash2, salt2 = service._hash_token('same_token')
        
        assert hash1 != hash2
        assert salt1 != salt2

    # ============================================================================
    # Tests for _build_reset_url()
    # ============================================================================

    def test_build_reset_url_uses_frontend_url_from_config(
        self,
        service,
        app_context
    ):
        """Test that _build_reset_url uses FRONTEND_URL from config."""
        from flask import current_app
        
        with patch.dict(current_app.config, {'FRONTEND_URL': 'https://example.com'}):
            url = service._build_reset_url('token123')
            assert url == 'https://example.com/reset-password?token=token123'

    def test_build_reset_url_uses_default_when_config_missing(
        self,
        service,
        app_context
    ):
        """Test that _build_reset_url uses default URL when config is missing."""
        url = service._build_reset_url('token456')
        
        # Should use default localhost URL
        assert url == 'http://localhost:5173/reset-password?token=token456'
