"""
Integration Tests for LoginService

Tests user login flow with email verification codes.
Uses real database and service instances - tests actual business logic, not mocks.
"""
from flask import current_app
import pytest
from unittest.mock import patch
from app.services.auth.login_service import LoginService
from app.models.user import User
from app.models.verification_code import VerificationCodeType, VerificationCode
from app.services.auth.verification_code_service import RateLimitExceededError
from app import db


@pytest.mark.integration
@pytest.mark.service
class TestLoginServiceIntegration:
    """Integration tests using REAL login service logic with actual database."""

    @pytest.fixture
    def service(self):
        """Create LoginService with REAL dependencies (only NotificationService mocked)."""
        with patch('app.services.auth.login_service.NotificationService'):
            service = LoginService()
        return service

    # ============================================================================
    # Tests for initiate_login()
    # ============================================================================

    def test_initiate_login_creates_login_code(
        self,
        service,
        verified_user,
        db_session
    ):
        service.initiate_login(email=verified_user.email)
        
        code = db_session.query(VerificationCode).filter_by(
            user_id=verified_user.user_id,
            code_type=VerificationCodeType.LOGIN.code
        ).first()
        
        assert code is not None
        assert code.is_used is False
        assert code.attempts == 0

    def test_initiate_login_sends_notification(
        self,
        service,
        verified_user
    ):
        captured_code = [None]
        original_notify = service.notification_service.send_verification_code
        def capture_code(**kwargs):
            captured_code[0] = kwargs.get('verification_code')
            return original_notify(**kwargs)
        
        service.notification_service.send_verification_code = capture_code
        
        service.initiate_login(email=verified_user.email)
        
        assert captured_code[0] is not None
        assert isinstance(captured_code[0], str)

    def test_initiate_login_nonexistent_user_raises_error(self, service):
        with pytest.raises(ValueError, match="User with this email does not exist"):
            service.initiate_login(email='nonexistent@example.com')

    def test_initiate_login_unverified_user_raises_error(
        self,
        service,
        unverified_user
    ):
        with pytest.raises(ValueError, match="User account is not verified"):
            service.initiate_login(email=unverified_user.email)

    def test_initiate_login_multiple_codes_per_user(
        self,
        service,
        verified_user,
        db_session
    ):
        captured_codes = []
        original_notify = service.notification_service.send_verification_code
        def capture_code(**kwargs):
            captured_codes.append(kwargs.get('verification_code'))
            return original_notify(**kwargs)
        
        service.notification_service.send_verification_code = capture_code
        
        service.initiate_login(email=verified_user.email)
        code1 = captured_codes[0]
        
        service.initiate_login(email=verified_user.email)
        code2 = captured_codes[1]
        
        assert code1 != code2
        
        codes = db_session.query(VerificationCode).filter_by(
            user_id=verified_user.user_id,
            code_type=VerificationCodeType.LOGIN.code
        ).all()
        assert len(codes) == 2

    # ============================================================================
    # Tests for verify_login()
    # ============================================================================

    def test_verify_login_valid_code_succeeds(
        self,
        service,
        verified_user,
        db_session
    ):
        captured_code = [None]
        original_notify = service.notification_service.send_verification_code
        def capture_code(**kwargs):
            captured_code[0] = kwargs.get('verification_code')
            return original_notify(**kwargs)
        
        service.notification_service.send_verification_code = capture_code
        
        service.initiate_login(email=verified_user.email)
        plain_code = captured_code[0]
        
        result = service.verify_login(
            email=verified_user.email,
            verification_code=plain_code
        )
        
        assert result is not None
        assert result.user_id == verified_user.user_id
        assert result.email == verified_user.email

    def test_verify_login_marks_code_as_used(
        self,
        service,
        verified_user,
        db_session
    ):
        captured_code = [None]
        original_notify = service.notification_service.send_verification_code
        def capture_code(**kwargs):
            captured_code[0] = kwargs.get('verification_code')
            return original_notify(**kwargs)
        
        service.notification_service.send_verification_code = capture_code
        
        service.initiate_login(email=verified_user.email)
        plain_code = captured_code[0]
        
        service.verify_login(email=verified_user.email, verification_code=plain_code)
        
        code_obj = db_session.query(VerificationCode).filter_by(
            user_id=verified_user.user_id,
            code_type=VerificationCodeType.LOGIN.code
        ).first()
        assert code_obj.is_used is True

    def test_verify_login_invalid_code_raises_error(
        self,
        service,
        verified_user
    ):
        service.initiate_login(email=verified_user.email)
        
        with pytest.raises(ValueError, match="Invalid or expired verification code"):
            service.verify_login(
                email=verified_user.email,
                verification_code='WRONGCODE'
            )

    def test_verify_login_nonexistent_user_raises_error(self, service):
        with pytest.raises(ValueError, match="User with this email does not exist"):
            service.verify_login(
                email='nonexistent@example.com',
                verification_code='ABC123'
            )

    def test_verify_login_unverified_user_raises_error(
        self,
        service,
        unverified_user
    ):
        with pytest.raises(ValueError, match="User account is not verified"):
            service.verify_login(
                email=unverified_user.email,
                verification_code='ABC123'
            )

    def test_verify_login_invalidates_other_codes(
        self,
        service,
        verified_user,
        db_session
    ):
        """Test that when a new login code is created, old codes are invalidated."""
        captured_codes = []
        original_notify = service.notification_service.send_verification_code
        def capture_code(**kwargs):
            captured_codes.append(kwargs.get('verification_code'))
            return original_notify(**kwargs)
        
        service.notification_service.send_verification_code = capture_code
        
        # Create first login code
        service.initiate_login(email=verified_user.email)
        code1 = captured_codes[0]
        
        # Get codes after first creation - code1 should be active
        codes_after_first = db_session.query(VerificationCode).filter_by(
            user_id=verified_user.user_id,
            code_type=VerificationCodeType.LOGIN.code
        ).all()
        assert len(codes_after_first) == 1
        assert codes_after_first[0].is_used is False
        
        # Create second login code - this should invalidate code1
        service.initiate_login(email=verified_user.email)
        code2 = captured_codes[1]
        
        # Get codes after second creation - both should exist, code1 should be used
        db_session.expire_all()
        codes_after_second = db_session.query(VerificationCode).filter_by(
            user_id=verified_user.user_id,
            code_type=VerificationCodeType.LOGIN.code
        ).all()
        assert len(codes_after_second) == 2
        
        # Old code should be marked as used
        code1_obj = next(c for c in codes_after_second if c.verification_code_id == codes_after_first[0].verification_code_id)
        assert code1_obj.is_used is True
        
        # New code should be unused
        code2_obj = next(c for c in codes_after_second if c.verification_code_id != codes_after_first[0].verification_code_id)
        assert code2_obj.is_used is False
        
        # Verify with new code should work
        result = service.verify_login(email=verified_user.email, verification_code=code2)
        assert result.user_id == verified_user.user_id
        assert code2_obj.is_used is True


    def test_initiate_login_exceeded_attempts_raises_error(
        self,
        service,
        verified_user,
        db_session,
        app_context
    ):
        """
        Test that exceeding max attempts prevents code verification
        This should raise RateLimitExceededError on further attempts.
        """
        wait_minutes = current_app.config.get('VERIFICATION_CODE_RATE_LIMIT_WINDOW_MINUTES', 60)
        max_codes = current_app.config.get('VERIFICATION_CODE_MAX_PER_HOUR', 3)
        for _ in range(max_codes):
            service.initiate_login(email=verified_user.email)
        
        with pytest.raises(RateLimitExceededError):
            service.initiate_login(email=verified_user.email)