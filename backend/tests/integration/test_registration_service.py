"""
Integration Tests for RegistrationService

Tests ACTUAL user registration, verification, and re-registration flows.
Uses real database and service instances - tests actual business logic, not mocks.
"""
import pytest
from unittest.mock import patch
from app.services.auth.registration_service import RegistrationService
from app.models.user import User, VerificationStatusEnum
from app.models.verification_code import VerificationCodeType, VerificationCode
from app import db


@pytest.mark.integration
@pytest.mark.service
class TestRegistrationServiceIntegration:
    """Integration tests using REAL service logic with actual database."""

    @pytest.fixture
    def service(self):
        """Create RegistrationService with REAL dependencies (only NotificationService mocked)."""
        with patch('app.services.auth.registration_service.NotificationService'):
            service = RegistrationService()
        return service

    # ============================================================================
    # Tests for register_user() - New User Registration
    # ============================================================================

    def test_register_new_user_creates_user_in_database(
        self,
        service,
        rotation_city,
        db_session
    ):
        result = service.register_user(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            rotation_city_id=rotation_city.city_id
        )
        
        assert result is not None
        assert result.first_name == 'John'
        assert result.last_name == 'Doe'
        assert result.email == 'john@example.com'
        assert result.is_verified is False
        
        db_user = db_session.query(User).filter_by(email='john@example.com').first()
        assert db_user is not None
        assert db_user.first_name == 'John'

    def test_register_new_user_creates_verification_code(
        self,
        service,
        rotation_city,
        db_session
    ):
        user = service.register_user(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            rotation_city_id=rotation_city.city_id
        )
        
        code = db_session.query(VerificationCode).filter_by(
            user_id=user.user_id,
            code_type=VerificationCodeType.REGISTRATION.code
        ).first()
        
        assert code is not None
        assert code.is_used is False
        assert code.attempts == 0

    def test_register_verified_user_raises_error_no_duplicate(
        self,
        service,
        rotation_city,
        db_session
    ):
        user1 = service.register_user(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            rotation_city_id=rotation_city.city_id
        )
        
        db_session.query(User).filter_by(user_id=user1.user_id).update({
            User.is_verified: True,
            User.status: VerificationStatusEnum.VERIFIED.code
        })
        db_session.commit()
        
        with pytest.raises(ValueError, match="User with this email already exists"):
            service.register_user(
                first_name='Jane',
                last_name='Smith',
                email='john@example.com',
                rotation_city_id=rotation_city.city_id
            )
        
        users = db_session.query(User).filter_by(email='john@example.com').all()
        assert len(users) == 1

    def test_register_unverified_user_returns_none_and_updates(
        self,
        service,
        rotation_city,
        db_session
    ):
        user1 = service.register_user(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            rotation_city_id=rotation_city.city_id
        )
        original_user_id = user1.user_id
        
        result = service.register_user(
            first_name='Jane',
            last_name='Smith',
            email='john@example.com',
            rotation_city_id=rotation_city.city_id
        )
        
        assert result is None
        
        db_user = db_session.query(User).filter_by(email='john@example.com').first()
        assert db_user.user_id == original_user_id
        assert db_user.first_name == 'Jane'
        assert db_user.last_name == 'Smith'

    def test_register_unverified_user_creates_new_code(
        self,
        service,
        rotation_city,
        db_session
    ):
        user1 = service.register_user(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            rotation_city_id=rotation_city.city_id
        )
        
        codes_before = db_session.query(VerificationCode).filter_by(
            user_id=user1.user_id
        ).all()
        assert len(codes_before) == 1
        first_code_id = codes_before[0].verification_code_id
        
        service.register_user(
            first_name='Jane',
            last_name='Smith',
            email='john@example.com',
            rotation_city_id=rotation_city.city_id
        )
        
        codes_after = db_session.query(VerificationCode).filter_by(
            user_id=user1.user_id
        ).all()
        assert len(codes_after) == 2
        
        first_code = db_session.query(VerificationCode).filter_by(
            verification_code_id=first_code_id
        ).first()
        assert first_code is not None

    # ============================================================================
    # Tests for verify_user_email()
    # ============================================================================

    def test_verify_user_email_valid_code_marks_verified(
        self,
        service,
        rotation_city,
        db_session
    ):
        captured_code = [None]
        original_notify = service.notification_service.send_verification_code
        def capture_code(**kwargs):
            captured_code[0] = kwargs.get('verification_code')
            return original_notify(**kwargs)
        
        service.notification_service.send_verification_code = capture_code
        
        user = service.register_user(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            rotation_city_id=rotation_city.city_id
        )
        
        plain_code = captured_code[0]
        assert plain_code is not None
        
        result = service.verify_user_email('john@example.com', plain_code)
        
        assert result is not None
        assert result.is_verified is True
        
        db_user = db_session.query(User).filter_by(email='john@example.com').first()
        assert db_user.is_verified is True
        assert db_user.status == VerificationStatusEnum.VERIFIED.code

    def test_verify_user_email_marks_code_as_used(
        self,
        service,
        rotation_city,
        db_session
    ):
        captured_code = [None]
        original_notify = service.notification_service.send_verification_code
        def capture_code(**kwargs):
            captured_code[0] = kwargs.get('verification_code')
            return original_notify(**kwargs)
        
        service.notification_service.send_verification_code = capture_code
        
        user = service.register_user(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            rotation_city_id=rotation_city.city_id
        )
        
        plain_code = captured_code[0]
        
        service.verify_user_email('john@example.com', plain_code)
        
        code_obj = db_session.query(VerificationCode).filter_by(
            user_id=user.user_id
        ).first()
        assert code_obj.is_used is True

    def test_verify_user_email_invalid_code_raises_error(
        self,
        service,
        rotation_city
    ):
        service.register_user(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            rotation_city_id=rotation_city.city_id
        )
        
        with pytest.raises(ValueError, match="Invalid or expired verification code"):
            service.verify_user_email('john@example.com', 'WRONGCODE')

    def test_verify_user_email_nonexistent_user_raises_error(self, service):
        with pytest.raises(ValueError, match="User with this email does not exist"):
            service.verify_user_email('nonexistent@example.com', 'ABC123')

    def test_verify_user_email_already_verified_raises_error(
        self,
        service,
        rotation_city,
        db_session
    ):
        captured_code = [None]
        original_notify = service.notification_service.send_verification_code
        def capture_code(**kwargs):
            captured_code[0] = kwargs.get('verification_code')
            return original_notify(**kwargs)
        
        service.notification_service.send_verification_code = capture_code
        
        user = service.register_user(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            rotation_city_id=rotation_city.city_id
        )
        
        plain_code = captured_code[0]
        service.verify_user_email('john@example.com', plain_code)
        
        with pytest.raises(ValueError, match="User is already verified"):
            service.verify_user_email('john@example.com', plain_code)

    def test_verify_code_invalidates_other_codes(
        self,
        service,
        rotation_city,
        db_session
    ):
        captured_codes = []
        original_notify = service.notification_service.send_verification_code
        def capture_code(**kwargs):
            captured_codes.append(kwargs.get('verification_code'))
            return original_notify(**kwargs)
        
        service.notification_service.send_verification_code = capture_code
        
        user = service.register_user(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            rotation_city_id=rotation_city.city_id
        )
        
        code1 = captured_codes[0]
        
        service.register_user(
            first_name='Jane',
            last_name='Smith',
            email='john@example.com',
            rotation_city_id=rotation_city.city_id
        )
        
        code2 = captured_codes[1]
        
        codes = db_session.query(VerificationCode).filter_by(
            user_id=user.user_id
        ).order_by(VerificationCode.created_at).all()
        assert len(codes) == 2
        assert codes[0].is_used is False
        assert codes[1].is_used is False
        
        service.verify_user_email('john@example.com', code2)
        
        db_session.expire_all()
        codes = db_session.query(VerificationCode).filter_by(
            user_id=user.user_id
        ).all()
        
        assert all(c.is_used for c in codes)

    def test_verify_code_increments_attempts_on_failure(
        self,
        service,
        rotation_city,
        db_session
    ):
        captured_code = [None]
        original_notify = service.notification_service.send_verification_code
        def capture_code(**kwargs):
            captured_code[0] = kwargs.get('verification_code')
            return original_notify(**kwargs)
        
        service.notification_service.send_verification_code = capture_code
        
        user = service.register_user(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            rotation_city_id=rotation_city.city_id
        )
        
        code_obj = db_session.query(VerificationCode).filter_by(
            user_id=user.user_id
        ).first()
        
        assert code_obj.attempts == 0
        
        try:
            service.verify_user_email('john@example.com', 'WRONG1')
        except ValueError:
            pass
        
        db_session.expire_all()
        code_obj = db_session.query(VerificationCode).filter_by(
            user_id=user.user_id
        ).first()
        assert code_obj.attempts == 1
        
        try:
            service.verify_user_email('john@example.com', 'WRONG2')
        except ValueError:
            pass
        
        db_session.expire_all()
        code_obj = db_session.query(VerificationCode).filter_by(
            user_id=user.user_id
        ).first()
        assert code_obj.attempts == 2

    # ============================================================================
    # Full Workflow Tests
    # ============================================================================

    def test_complete_registration_verification_workflow(
        self,
        service,
        rotation_city,
        db_session
    ):
        captured_code = [None]
        original_notify = service.notification_service.send_verification_code
        def capture_code(**kwargs):
            captured_code[0] = kwargs.get('verification_code')
            return original_notify(**kwargs)
        
        service.notification_service.send_verification_code = capture_code
        
        user = service.register_user(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            rotation_city_id=rotation_city.city_id
        )
        
        assert user is not None
        assert user.is_verified is False
        
        plain_code = captured_code[0]
        assert plain_code is not None
        
        verified_user = service.verify_user_email('john@example.com', plain_code)
        
        assert verified_user.is_verified is True
        assert verified_user.status == VerificationStatusEnum.VERIFIED.code
        
        db_user = db_session.query(User).filter_by(email='john@example.com').first()
        assert db_user.is_verified is True

    def test_re_registration_new_verification_workflow(
        self,
        service,
        rotation_city,
        db_session
    ):
        captured_codes = []
        original_notify = service.notification_service.send_verification_code
        def capture_code(**kwargs):
            captured_codes.append(kwargs.get('verification_code'))
            return original_notify(**kwargs)
        
        service.notification_service.send_verification_code = capture_code
        
        user1 = service.register_user(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            rotation_city_id=rotation_city.city_id
        )
        
        code1 = captured_codes[0]
        
        result = service.register_user(
            first_name='Jane',
            last_name='Smith',
            email='john@example.com',
            rotation_city_id=rotation_city.city_id
        )
        
        assert result is None
        code2 = captured_codes[1]
        
        with pytest.raises(ValueError, match="Invalid or expired verification code"):
            service.verify_user_email('john@example.com', code1)
        
        verified_user = service.verify_user_email('john@example.com', code2)
        
        assert verified_user.is_verified is True
        
        db_user = db_session.query(User).filter_by(email='john@example.com').first()
        assert db_user.first_name == 'Jane'
        assert db_user.last_name == 'Smith'
        assert db_user.is_verified is True
