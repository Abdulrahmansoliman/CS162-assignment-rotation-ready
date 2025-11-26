"""
Integration Tests for PasswordResetService

Tests ACTUAL password reset flow with real database.
Uses real database and service instances - tests actual business logic, not mocks.
"""
import pytest
from unittest.mock import patch
from datetime import datetime, timedelta
from app.services.auth.password_reset_service import (
    PasswordResetService,
    InvalidOrExpiredTokenError
)
from app.models.user import User
from app.models.verification_code import VerificationCode, VerificationCodeType
from app.repositories.implementations.user_repository import UserRepository
from app import db


@pytest.mark.integration
@pytest.mark.service
class TestPasswordResetServiceIntegration:
    """Integration tests using REAL service logic with actual database."""

    @pytest.fixture
    def service(self):
        """Create PasswordResetService with REAL dependencies (only NotificationService mocked)."""
        with patch('app.services.auth.password_reset_service.NotificationService'):
            service = PasswordResetService()
        return service

    @pytest.fixture
    def verified_user(self, rotation_city, db_session):
        """Create a verified user with password in the database."""
        user_repo = UserRepository()
        user = user_repo.create_user(
            first_name='Jane',
            last_name='Doe',
            email='jane@example.com',
            rotation_city_id=rotation_city.city_id
        )
        user.set_password('oldpassword123')
        user.is_verified = True
        db_session.commit()
        db_session.refresh(user)
        return user

    # ============================================================================
    # Tests for request_reset() - Request Password Reset
    # ============================================================================

    def test_request_reset_creates_verification_code_in_database(
        self,
        service,
        verified_user,
        db_session
    ):
        """Test that request_reset creates a password reset code in database."""
        service.request_reset(verified_user.email)
        
        code = db_session.query(VerificationCode).filter_by(
            user_id=verified_user.user_id,
            code_type=VerificationCodeType.PASSWORD_RESET.code
        ).first()
        
        assert code is not None
        assert code.is_used is False
        assert code.attempts == 0
        assert code.expires_at > datetime.utcnow()

    def test_request_reset_invalidates_previous_codes(
        self,
        service,
        verified_user,
        db_session
    ):
        """Test that requesting reset invalidates previous reset codes."""
        # Create first reset request
        service.request_reset(verified_user.email)
        first_code = db_session.query(VerificationCode).filter_by(
            user_id=verified_user.user_id,
            code_type=VerificationCodeType.PASSWORD_RESET.code
        ).first()
        
        # Create second reset request
        service.request_reset(verified_user.email)
        
        # Refresh first code from database
        db_session.refresh(first_code)
        
        # First code should be marked as used
        assert first_code.is_used is True

    def test_request_reset_does_not_fail_for_nonexistent_user(
        self,
        service
    ):
        """Test that request_reset doesn't raise error for non-existent email."""
        # Should not raise any exception (prevents email enumeration)
        service.request_reset('nonexistent@example.com')

    def test_request_reset_sets_correct_expiry_time(
        self,
        service,
        verified_user,
        db_session,
        app_context
    ):
        """Test that reset code has correct expiry time from config."""
        service.request_reset(verified_user.email)
        
        code = db_session.query(VerificationCode).filter_by(
            user_id=verified_user.user_id,
            code_type=VerificationCodeType.PASSWORD_RESET.code,
            is_used=False
        ).first()
        
        # Check that expiry is approximately 15 minutes from now (default config)
        time_diff = code.expires_at - datetime.utcnow()
        assert 14 <= time_diff.total_seconds() / 60 <= 16  # Allow 1 min margin

    # ============================================================================
    # Tests for confirm_reset() - Confirm Password Reset
    # ============================================================================

    @patch('app.services.auth.password_reset_service.secrets.token_urlsafe')
    def test_confirm_reset_updates_user_password(
        self,
        mock_token,
        service,
        verified_user,
        db_session
    ):
        """Test that confirm_reset successfully updates user password."""
        mock_token.return_value = 'test_reset_token'
        
        # Request reset
        service.request_reset(verified_user.email)
        
        # Confirm reset with new password
        service.confirm_reset('test_reset_token', 'newpassword456')
        
        # Refresh user and verify password changed
        db_session.refresh(verified_user)
        assert verified_user.check_password('newpassword456') is True
        assert verified_user.check_password('oldpassword123') is False

    @patch('app.services.auth.password_reset_service.secrets.token_urlsafe')
    def test_confirm_reset_marks_code_as_used(
        self,
        mock_token,
        service,
        verified_user,
        db_session
    ):
        """Test that confirm_reset marks verification code as used."""
        mock_token.return_value = 'test_reset_token'
        
        service.request_reset(verified_user.email)
        service.confirm_reset('test_reset_token', 'newpassword456')
        
        code = db_session.query(VerificationCode).filter_by(
            user_id=verified_user.user_id,
            code_type=VerificationCodeType.PASSWORD_RESET.code
        ).first()
        
        assert code.is_used is True
        assert code.used_at is not None

    def test_confirm_reset_raises_error_for_invalid_token(
        self,
        service,
        verified_user
    ):
        """Test that confirm_reset raises error for invalid token."""
        service.request_reset(verified_user.email)
        
        with pytest.raises(InvalidOrExpiredTokenError):
            service.confirm_reset('invalid_token', 'newpassword456')

    @patch('app.services.auth.password_reset_service.secrets.token_urlsafe')
    def test_confirm_reset_raises_error_for_used_token(
        self,
        mock_token,
        service,
        verified_user
    ):
        """Test that confirm_reset raises error when token is already used."""
        mock_token.return_value = 'test_reset_token'
        
        service.request_reset(verified_user.email)
        service.confirm_reset('test_reset_token', 'newpassword456')
        
        # Try to use same token again
        with pytest.raises(InvalidOrExpiredTokenError):
            service.confirm_reset('test_reset_token', 'anotherpassword')

    def test_confirm_reset_raises_error_for_expired_token(
        self,
        service,
        verified_user,
        db_session
    ):
        """Test that confirm_reset raises error for expired token."""
        service.request_reset(verified_user.email)
        
        # Manually expire the code
        code = db_session.query(VerificationCode).filter_by(
            user_id=verified_user.user_id,
            code_type=VerificationCodeType.PASSWORD_RESET.code,
            is_used=False
        ).first()
        
        code.expires_at = datetime.utcnow() - timedelta(minutes=1)
        db_session.commit()
        
        with pytest.raises(InvalidOrExpiredTokenError):
            service.confirm_reset('any_token', 'newpassword456')

    # ============================================================================
    # Tests for Complete Password Reset Flow
    # ============================================================================

    @patch('app.services.auth.password_reset_service.secrets.token_urlsafe')
    def test_complete_password_reset_flow(
        self,
        mock_token,
        service,
        verified_user,
        db_session
    ):
        """Test complete password reset flow from request to confirmation."""
        mock_token.return_value = 'complete_flow_token'
        
        # Step 1: User requests password reset
        service.request_reset(verified_user.email)
        
        # Verify code was created
        code = db_session.query(VerificationCode).filter_by(
            user_id=verified_user.user_id,
            code_type=VerificationCodeType.PASSWORD_RESET.code,
            is_used=False
        ).first()
        assert code is not None
        
        # Step 2: User confirms reset with token
        service.confirm_reset('complete_flow_token', 'brandnewpassword')
        
        # Verify password was updated
        db_session.refresh(verified_user)
        assert verified_user.check_password('brandnewpassword') is True
        
        # Verify code was marked as used
        db_session.refresh(code)
        assert code.is_used is True

    @patch('app.services.auth.password_reset_service.secrets.token_urlsafe')
    def test_multiple_reset_requests_only_latest_valid(
        self,
        mock_token,
        service,
        verified_user,
        db_session
    ):
        """Test that only the latest reset token is valid."""
        # First reset request
        mock_token.return_value = 'first_token'
        service.request_reset(verified_user.email)
        
        # Second reset request
        mock_token.return_value = 'second_token'
        service.request_reset(verified_user.email)
        
        # First token should not work
        with pytest.raises(InvalidOrExpiredTokenError):
            service.confirm_reset('first_token', 'newpassword')
        
        # Second token should work
        service.confirm_reset('second_token', 'newpassword')
        
        db_session.refresh(verified_user)
        assert verified_user.check_password('newpassword') is True
