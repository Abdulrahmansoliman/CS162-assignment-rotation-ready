"""
Integration Tests for Email Verification Rate Limiting

Tests the rate limiting functionality for verification code requests.
"""
import pytest
from unittest.mock import patch
from app.services.auth.registration_service import RegistrationService
from app.services.auth.verification_code_service import RateLimitExceededError
from app.models.user import User
from app import db


@pytest.mark.integration
@pytest.mark.service
class TestVerificationCodeRateLimiting:
    """Integration tests for verification code rate limiting."""

    @pytest.fixture
    def service(self):
        """Create RegistrationService with mocked NotificationService."""
        with patch('app.services.auth.registration_service.NotificationService'):
            service = RegistrationService()
        return service

    # ============================================================================
    # Tests for Registration Rate Limiting
    # ============================================================================

    def test_user_can_register_within_rate_limit(
        self,
        service,
        rotation_city,
        app_context
    ):
        """Test that user can register successfully within rate limit."""
        user = service.register_user(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            rotation_city_id=rotation_city.city_id
        )
        
        assert user is not None
        assert user.email == 'john@example.com'

    def test_multiple_registrations_same_user_respects_rate_limit(
        self,
        service,
        rotation_city,
        app_context
    ):
        """Test that multiple registration attempts for same user are rate limited."""
        # First registration should succeed
        user1 = service.register_user(
            first_name='Jane',
            last_name='Smith',
            email='jane@example.com',
            rotation_city_id=rotation_city.city_id
        )
        assert user1 is not None
        
        # Second attempt (resend code) should succeed
        user2 = service.register_user(
            first_name='Jane',
            last_name='Smith',
            email='jane@example.com',
            rotation_city_id=rotation_city.city_id
        )
        assert user2 is None  # Returns None for resend
        
        # Third attempt should succeed
        user3 = service.register_user(
            first_name='Jane',
            last_name='Smith',
            email='jane@example.com',
            rotation_city_id=rotation_city.city_id
        )
        assert user3 is None
        
        # Fourth attempt should be rate limited (exceeds max of 3 per hour)
        with pytest.raises(RateLimitExceededError) as exc_info:
            service.register_user(
                first_name='Jane',
                last_name='Smith',
                email='jane@example.com',
                rotation_city_id=rotation_city.city_id
            )
        
        assert 'Too many verification code requests' in str(exc_info.value)

    def test_resend_code_respects_rate_limit(
        self,
        service,
        rotation_city,
        app_context
    ):
        """Test that resending verification codes is rate limited."""
        # Initial registration
        user = service.register_user(
            first_name='Bob',
            last_name='Johnson',
            email='bob@example.com',
            rotation_city_id=rotation_city.city_id
        )
        assert user is not None
        
        # First resend should succeed
        service.resend_verification_code('bob@example.com')
        
        # Second resend should succeed
        service.resend_verification_code('bob@example.com')
        
        # Third resend should be rate limited (total 4 codes in 1 hour)
        with pytest.raises(RateLimitExceededError):
            service.resend_verification_code('bob@example.com')

    def test_rate_limit_is_per_user(
        self,
        service,
        rotation_city,
        app_context
    ):
        """Test that rate limiting is applied per user, not globally."""
        # User 1 makes 3 requests (at the limit)
        user1 = service.register_user(
            first_name='Alice',
            last_name='Wonder',
            email='alice@example.com',
            rotation_city_id=rotation_city.city_id
        )
        assert user1 is not None
        
        service.register_user(
            first_name='Alice',
            last_name='Wonder',
            email='alice@example.com',
            rotation_city_id=rotation_city.city_id
        )
        
        service.register_user(
            first_name='Alice',
            last_name='Wonder',
            email='alice@example.com',
            rotation_city_id=rotation_city.city_id
        )
        
        # User 1's next request should be rate limited
        with pytest.raises(RateLimitExceededError):
            service.register_user(
                first_name='Alice',
                last_name='Wonder',
                email='alice@example.com',
                rotation_city_id=rotation_city.city_id
            )
        
        # User 2 should still be able to register
        user2 = service.register_user(
            first_name='Bob',
            last_name='Builder',
            email='bob@example.com',
            rotation_city_id=rotation_city.city_id
        )
        assert user2 is not None

    def test_rate_limit_separate_for_registration_and_login(
        self,
        service,
        rotation_city,
        db_session,
        app_context
    ):
        """Test that registration and login have separate rate limits."""
        from app.repositories.implementations.user_repository import UserRepository
        from app.services.auth.login_service import LoginService
        
        # Create and verify a user
        user = service.register_user(
            first_name='Charlie',
            last_name='Brown',
            email='charlie@example.com',
            rotation_city_id=rotation_city.city_id
        )
        
        user_repo = UserRepository()
        user_repo.mark_user_as_verified(user.user_id)
        
        # Make 3 registration attempts for another email
        for i in range(3):
            try:
                service.register_user(
                    first_name='Test',
                    last_name='User',
                    email='test@example.com',
                    rotation_city_id=rotation_city.city_id
                )
            except RateLimitExceededError:
                pass
        
        # Login requests for the verified user should still work
        # because they have separate rate limits
        with patch('app.services.auth.login_service.NotificationService'):
            login_service = LoginService()
            # This should not raise RateLimitExceededError
            login_service.initiate_login('charlie@example.com')
