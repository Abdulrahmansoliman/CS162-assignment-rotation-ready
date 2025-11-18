"""
Unit tests for VerificationCodeRepository.
"""
import pytest
from app.repositories.verification_code_repository import VerificationCodeRepository
from app.models import VerificationCodeType


@pytest.mark.unit
@pytest.mark.repository
class TestVerificationCodeRepository:
    """Test cases for VerificationCodeRepository."""
    
    def test_create_registration_code(self, db_session, user):
        """Test creating a new registration verification code for a user.
        
        This test:
        1. Creates a registration code using the repository
        2. Verifies it's saved to the database
        3. Checks the attributes are correct
        """
        # Arrange (Setup)
        code_hash = "test_hash_12345"
        hash_salt = "test_salt_12345"   
        
        # Act (Execute)
        verification_code = VerificationCodeRepository.create_registration(
            user_id=user.user_id,
            code_hash=code_hash,
            hash_salt=hash_salt
        )
        
        # Assert (Verify)
        assert verification_code is not None
        assert verification_code.id is not None
        assert verification_code.user_id == user.user_id
        assert verification_code.code_hash == code_hash
        assert verification_code.hash_salt == hash_salt
        assert verification_code.code_type == VerificationCodeType.REGISTRATION.code
        assert verification_code.is_used is False

    def test_create_login_code(self, db_session, user):
        """Test creating a new login verification code for a user.
        
        This test:
        1. Creates a login code using the repository
        2. Verifies it's saved to the database
        3. Checks the attributes are correct
        """
        # Arrange (Setup)
        code_hash = "login_hash_67890"
        hash_salt = "login_salt_67890"   
        
        # Act (Execute)
        verification_code = VerificationCodeRepository.create_login(
            user_id=user.user_id,
            code_hash=code_hash,
            hash_salt=hash_salt
        )
        
        # Assert (Verify)
        assert verification_code is not None
        assert verification_code.id is not None
        assert verification_code.user_id == user.user_id
        assert verification_code.code_hash == code_hash
        assert verification_code.hash_salt == hash_salt
        assert verification_code.code_type == VerificationCodeType.LOGIN.code
        assert verification_code.is_used is False

    def test_increase_attempts(self, registration_code):
        """Test increasing the attempt count for a verification code.
        
        This test:
        1. Increases the attempts for an existing code
        2. Verifies the attempts count is incremented
        """
        # Arrange (Setup)
        initial_attempts = registration_code.attempts
        
        # Act (Execute)
        VerificationCodeRepository.increase_attempts(registration_code.id)
        
        # Refresh from DB
        new_attempts = registration_code.attempts
        
        # Assert (Verify)
        assert new_attempts == initial_attempts + 1

    def test_mark_code_as_used(self, registration_code):
        """Test marking a verification code as used.
        
        This test:
        1. Marks an existing code as used
        2. Verifies the is_used flag is set to True
        """
        # Arrange (Setup)
        assert registration_code.is_used is False
        
        # Act (Execute)
        VerificationCodeRepository.mark_code_as_used(registration_code.id)
        
        # Refresh from DB
        is_used = registration_code.is_used
        
        # Assert (Verify)
        assert is_used is True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
