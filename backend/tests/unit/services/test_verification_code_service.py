"""
Unit tests for VerificationCodeService with mocked dependencies.
"""
import pytest
from unittest.mock import Mock, patch
from app.services.auth.verification_code_service import (
    VerificationCodeService
)
from app.models.verification_code import VerificationCode, VerificationCodeType
from app.models.user import User


@pytest.mark.unit
@pytest.mark.service
class TestVerificationCodeService:
    """Test cases for VerificationCodeService."""

    @pytest.fixture
    def mock_repo(self):
        """Provide a mocked VerificationCodeRepository."""
        return Mock()

    @pytest.fixture
    def service(self, mock_repo):
        """Provide VerificationCodeService with mocked repository."""
        return VerificationCodeService(
            verification_code_repository=mock_repo
        )

    @pytest.fixture
    def sample_user(self):
        """Provide a sample user for testing."""
        return User(
            user_id=1,
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            rotation_city_id=1
        )

    def test_create_registration_code(
        self,
        service,
        mock_repo,
        sample_user,
        app
    ):
        """Test creating a registration verification code."""
        # Arrange
        mock_code = VerificationCode(
            id=1,
            user_id=sample_user.user_id,
            code_hash="hash123",
            hash_salt="salt123",
            code_type=VerificationCodeType.REGISTRATION.code
        )
        mock_repo.create_registration.return_value = mock_code

        # Act
        result_code, plain_code = service.create_registration_code(
            sample_user
        )

        # Assert
        assert result_code is not None
        assert plain_code is not None
        assert len(plain_code) == app.config.get(
            'VERIFICATION_CODE_LENGTH',
            6
        )
        mock_repo.create_registration.assert_called_once()

    def test_verify_registration_code_success(
        self,
        service,
        mock_repo,
        sample_user,
        app
    ):
        """Test successful verification of registration code."""
        # Arrange
        mock_code = VerificationCode(
            id=1,
            user_id=sample_user.user_id,
            code_hash=(
                "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
            ),
            hash_salt="salt123",
            code_type=VerificationCodeType.REGISTRATION.code,
            verification_code_id=1
        )
        mock_repo.find_most_recent_active_code.return_value = mock_code

        with patch.object(
            service,
            '_validate_code',
            return_value=True
        ):
            # Act
            result = service.verify_registration_code(
                sample_user,
                "ABC123"
            )

            # Assert
            assert result is True
            mock_repo.mark_as_used.assert_called_once_with(1)
            mock_repo.invalidate_user_codes.assert_called_once()

    def test_verify_registration_code_no_code_found(
        self,
        service,
        mock_repo,
        sample_user
    ):
        """Test verification fails when no active code exists."""
        # Arrange
        mock_repo.find_most_recent_active_code.return_value = None

        # Act
        result = service.verify_registration_code(sample_user, "ABC123")

        # Assert
        assert result is False
        mock_repo.mark_as_used.assert_not_called()

    def test_verify_registration_code_invalid_code(
        self,
        service,
        mock_repo,
        sample_user
    ):
        """Test verification fails with invalid code."""
        # Arrange
        mock_code = VerificationCode(
            id=1,
            user_id=sample_user.user_id,
            code_hash="hash123",
            hash_salt="salt123",
            code_type=VerificationCodeType.REGISTRATION.code,
            verification_code_id=1
        )
        mock_repo.find_most_recent_active_code.return_value = mock_code

        with patch.object(
            service,
            '_validate_code',
            return_value=False
        ):
            # Act
            result = service.verify_registration_code(
                sample_user,
                "WRONG123"
            )

            # Assert
            assert result is False
            mock_repo.increase_attempts.assert_called_once_with(1)
            mock_repo.mark_as_used.assert_not_called()

    def test_verify_login_code_success(
        self,
        service,
        mock_repo,
        sample_user
    ):
        """Test successful verification of login code."""
        # Arrange
        mock_code = VerificationCode(
            id=2,
            user_id=sample_user.user_id,
            code_hash="loginhash",
            hash_salt="loginsalt",
            code_type=VerificationCodeType.LOGIN.code,
            verification_code_id=2
        )
        mock_repo.find_most_recent_active_code.return_value = mock_code

        with patch.object(
            service,
            '_validate_code',
            return_value=True
        ):
            # Act
            result = service.verify_login_code(sample_user, "XYZ789")

            # Assert
            assert result is True
            mock_repo.mark_as_used.assert_called_once_with(2)

    def test_hash_code_generates_unique_hashes(
        self,
        service,
        app
    ):
        """Test that hash_code generates unique hashes for same code."""
        # Act
        hash1, salt1 = service._hash_code("ABC123")
        hash2, salt2 = service._hash_code("ABC123")

        # Assert
        assert salt1 != salt2
        assert hash1 != hash2

    def test_generate_code_correct_length(
        self,
        service,
        app
    ):
        """Test that generated code has correct length."""
        # Act
        code = service._generate_code()

        # Assert
        expected_length = app.config.get('VERIFICATION_CODE_LENGTH', 6)
        assert len(code) == expected_length
        assert code.isalnum()
        assert code.isupper() or code.isdigit()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
