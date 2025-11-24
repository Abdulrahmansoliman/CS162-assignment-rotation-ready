"""
Integration Tests for LoginService

Tests user login flow with email verification codes.
Uses real database and service instances - tests actual business logic, not mocks.
"""
import pytest
from unittest.mock import patch
from app.services.auth.login_service import LoginService
from app.models.user import User
from app.models.verification_code import VerificationCodeType, VerificationCode
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
