"""
Unit tests for RegistrationService with mocked dependencies.
"""
import pytest
from unittest.mock import Mock, MagicMock
from app.services.auth.registration_service import RegistrationService
from app.models.user import User
from app.models.verification_status_enum import VerificationStatusEnum


@pytest.mark.unit
@pytest.mark.service
class TestRegistrationService:
    """Test cases for RegistrationService with dependency injection."""

    @pytest.fixture
    def mock_user_repo(self):
        """Provide a mocked UserRepository."""
        return Mock()

    @pytest.fixture
    def mock_verification_repo(self):
        """Provide a mocked VerificationCodeRepository."""
        return Mock()

    @pytest.fixture
    def service(self, mock_user_repo, mock_verification_repo):
        """Provide RegistrationService with mocked dependencies."""
        return RegistrationService(
            user_repository=mock_user_repo,
            verification_code_repository=mock_verification_repo
        )

    def test_register_new_user_success(
        self,
        service,
        mock_user_repo,
        mock_verification_repo,
        app
    ):
        """Test successful registration of a new user."""
        # Arrange
        mock_user_repo.get_user_by_email.return_value = None
        
        new_user = User(
            user_id=1,
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            rotation_city_id=1,
            is_verified=False,
            status=VerificationStatusEnum.PENDING.code
        )
        mock_user_repo.create_user.return_value = new_user

        # Act
        result = service.register_user(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            rotation_city_id=1
        )

        # Assert
        assert result is not None
        assert result.email == "john@example.com"
        mock_user_repo.get_user_by_email.assert_called_once_with(
            "john@example.com"
        )
        mock_user_repo.create_user.assert_called_once()

    def test_register_user_already_verified(
        self,
        service,
        mock_user_repo
    ):
        """Test registration fails when user already exists and verified."""
        # Arrange
        existing_user = User(
            user_id=1,
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            rotation_city_id=1,
            is_verified=True,
            status=VerificationStatusEnum.VERIFIED.code
        )
        mock_user_repo.get_user_by_email.return_value = existing_user

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            service.register_user(
                first_name="John",
                last_name="Doe",
                email="john@example.com",
                rotation_city_id=1
            )

        assert "already exists" in str(exc_info.value)
        mock_user_repo.create_user.assert_not_called()

    def test_register_user_unverified_existing(
        self,
        service,
        mock_user_repo,
        app
    ):
        """Test registration with unverified existing user."""
        # Arrange
        existing_user = User(
            user_id=1,
            first_name="OldFirst",
            last_name="OldLast",
            email="john@example.com",
            rotation_city_id=1,
            is_verified=False,
            status=VerificationStatusEnum.PENDING.code
        )
        mock_user_repo.get_user_by_email.return_value = existing_user

        # Act
        result = service.register_user(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            rotation_city_id=2
        )

        # Assert
        assert result is None
        mock_user_repo.update.assert_called_once()
        mock_user_repo.create_user.assert_not_called()

    def test_verify_user_email_success(
        self,
        service,
        mock_user_repo
    ):
        """Test successful email verification."""
        # Arrange
        user = User(
            user_id=1,
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            rotation_city_id=1,
            is_verified=False,
            status=VerificationStatusEnum.PENDING.code
        )
        mock_user_repo.get_user_by_email.return_value = user
        
        # Mock the verification service's method
        service.verification_service.verify_registration_code = Mock(
            return_value=True
        )

        # Act
        result = service.verify_user_email(
            email="john@example.com",
            verification_code="ABC123"
        )

        # Assert
        assert result is not None
        mock_user_repo.mark_user_as_verified.assert_called_once_with(
            user.user_id
        )

    def test_verify_user_email_user_not_found(
        self,
        service,
        mock_user_repo
    ):
        """Test verification fails when user doesn't exist."""
        # Arrange
        mock_user_repo.get_user_by_email.return_value = None

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            service.verify_user_email(
                email="nonexistent@example.com",
                verification_code="ABC123"
            )

        assert "does not exist" in str(exc_info.value)

    def test_verify_user_email_already_verified(
        self,
        service,
        mock_user_repo
    ):
        """Test verification fails when user is already verified."""
        # Arrange
        user = User(
            user_id=1,
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            rotation_city_id=1,
            is_verified=True,
            status=VerificationStatusEnum.VERIFIED.code
        )
        mock_user_repo.get_user_by_email.return_value = user

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            service.verify_user_email(
                email="john@example.com",
                verification_code="ABC123"
            )

        assert "already verified" in str(exc_info.value)

    def test_verify_user_email_invalid_code(
        self,
        service,
        mock_user_repo
    ):
        """Test verification fails with invalid code."""
        # Arrange
        user = User(
            user_id=1,
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            rotation_city_id=1,
            is_verified=False,
            status=VerificationStatusEnum.PENDING.code
        )
        mock_user_repo.get_user_by_email.return_value = user
        
        # Mock the verification service's method
        service.verification_service.verify_registration_code = Mock(
            return_value=False
        )

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            service.verify_user_email(
                email="john@example.com",
                verification_code="WRONG123"
            )

        assert "Invalid or expired" in str(exc_info.value)
        mock_user_repo.mark_user_as_verified.assert_not_called()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
