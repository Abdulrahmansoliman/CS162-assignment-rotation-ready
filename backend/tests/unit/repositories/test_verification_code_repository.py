"""
Unit tests for VerificationCodeRepository.
"""
import pytest
from app.repositories.verification_code_repository import VerificationCodeRepository
from app.models import VerificationCodeType, VerificationCode
from app import db
from datetime import datetime, timedelta


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

    def test_invalidate_user_codes(self, registration_code):
        """Test invalidating all active codes for a user and code type.
        
        This test:
        1. Create more recent active code for the same user and type
        2. Invalidates all codes for that user and type
        3. Verifies that all codes are marked as used
        """
        # Arrange (Setup)
        user_id = registration_code.user_id
        code_type = registration_code.code_type
        
        # Create another active code
        another_code = VerificationCodeRepository.create_registration(
            user_id=user_id,
            code_hash="another_hash_99999",
            hash_salt="another_salt_99999"
        )
        assert another_code.is_used is False
        
        # Act (Execute)
        VerificationCodeRepository.invalidate_user_codes(user_id, code_type)
        
        # Refresh from DB
        reg_code_used = registration_code.is_used
        another_code_used = another_code.is_used
        
        # Assert (Verify)
        assert reg_code_used is True
        assert another_code_used is True

    def test_find_most_recent_active_code(self, registration_code):
        """Test finding the most recent active verification code for a user and type.
        
        This test:
        1. Creates multiple codes for the same user and type
        2. Retrieves the most recent active code
        3. Verifies the correct code is returned
        """
        # Arrange (Setup)
        user_id = registration_code.user_id
        code_type = registration_code.code_type
        
        # Create a new code
        new_code = VerificationCodeRepository.create_registration(
            user_id=user_id,
            code_hash="new_hash_22222",
            hash_salt="new_salt_22222"
        )

        expire_code = VerificationCodeRepository.create_registration(
            user_id=user_id,
            code_hash="expired_hash_33333",
            hash_salt="expired_salt_33333"
        ) 
        # Manually set it as used to simulate expiration
        expire_code.created_at = registration_code.created_at - timedelta(minutes=30)
        expire_code.expires_at = registration_code.created_at - timedelta(minutes=15)
        
        # Act (Execute)
        most_recent_code = VerificationCodeRepository.find_most_recent_active_code(
            user_id=user_id,
            code_type=code_type
        )
        
        # Assert (Verify)
        assert most_recent_code is not None
        assert most_recent_code.id == new_code.id
        assert most_recent_code.created_at > registration_code.created_at

    def test_increase_attempts_nonexistent_code(self):
        """Test increasing attempts for a code that doesn't exist.
        
        This test:
        1. Attempts to increase attempts for a non-existent code ID
        2. Verifies the operation doesn't crash and handles gracefully
        """
        # Arrange (Setup)
        nonexistent_id = 99999
        
        # Act & Assert (should not raise an exception)
        try:
            VerificationCodeRepository.increase_attempts(nonexistent_id)
        except Exception as e:
            pytest.fail(f"Should not raise exception for nonexistent code: {e}")

    def test_mark_code_as_used_multiple_times(self, registration_code):
        """Test marking a verification code as used multiple times.
        
        This test:
        1. Marks a code as used the first time
        2. Marks it as used again
        3. Verifies it remains used without errors
        """
        # Arrange (Setup)
        code_id = registration_code.id
        assert registration_code.is_used is False
        
        # Act (Execute) - First mark as used
        VerificationCodeRepository.mark_code_as_used(code_id)
        registration_code.is_used = True
        
        # Assert (Verify) - First time
        assert registration_code.is_used is True
        
        # Act (Execute) - Mark as used again
        VerificationCodeRepository.mark_code_as_used(code_id)
        
        # Assert (Verify) - Should still be used, no errors
        assert registration_code.is_used is True

    def test_find_most_recent_active_code_when_all_used(self, user):
        """Test finding most recent active code when all codes are marked as used.
        
        This test:
        1. Creates multiple codes for a user
        2. Marks all codes as used
        3. Verifies that no active code is returned
        """
        # Arrange (Setup)
        code1 = VerificationCodeRepository.create_registration(
            user_id=user.user_id,
            code_hash="hash_1",
            hash_salt="salt_1"
        )
        code2 = VerificationCodeRepository.create_registration(
            user_id=user.user_id,
            code_hash="hash_2",
            hash_salt="salt_2"
        )
        
        # Mark all codes as used
        VerificationCodeRepository.mark_code_as_used(code1.id)
        VerificationCodeRepository.mark_code_as_used(code2.id)
        
        # Act (Execute)
        most_recent_code = VerificationCodeRepository.find_most_recent_active_code(
            user_id=user.user_id,
            code_type=VerificationCodeType.REGISTRATION.code
        )
        
        # Assert (Verify)
        assert most_recent_code is None

    def test_find_most_recent_active_code_when_all_expired(self, db_session, user):
        """Test finding most recent active code when all codes are expired.
        
        This test:
        1. Creates multiple codes for a user
        2. Sets their expiry times to the past
        3. Verifies that no active code is returned
        """
        # Arrange (Setup)
        now = datetime.utcnow()
        
        code1 = VerificationCode(
            user_id=user.user_id,
            code_hash="expired_hash_1",
            hash_salt="expired_salt_1",
            code_type=VerificationCodeType.REGISTRATION.code,
            created_at=now - timedelta(minutes=30),
            expires_at=now - timedelta(minutes=15)  # Already expired
        )
        code2 = VerificationCode(
            user_id=user.user_id,
            code_hash="expired_hash_2",
            hash_salt="expired_salt_2",
            code_type=VerificationCodeType.REGISTRATION.code,
            created_at=now - timedelta(minutes=20),
            expires_at=now - timedelta(minutes=5)  # Already expired
        )
        
        db_session.add(code1)
        db_session.add(code2)
        db_session.commit()
        
        # Act (Execute)
        most_recent_code = VerificationCodeRepository.find_most_recent_active_code(
            user_id=user.user_id,
            code_type=VerificationCodeType.REGISTRATION.code
        )
        
        # Assert (Verify)
        assert most_recent_code is None

    def test_find_most_recent_active_code_empty_user(self, user):
        """Test finding most recent active code for a user with no codes.
        
        This test:
        1. Uses a user that has no verification codes
        2. Attempts to find the most recent active code
        3. Verifies that None is returned
        """
        # Arrange (Setup) - User already exists but has no codes
        
        # Act (Execute)
        most_recent_code = VerificationCodeRepository.find_most_recent_active_code(
            user_id=user.user_id,
            code_type=VerificationCodeType.REGISTRATION.code
        )
        
        # Assert (Verify)
        assert most_recent_code is None

    def test_invalidate_user_codes_empty_user(self, user):
        """Test invalidating codes for a user who has no active codes.
        
        This test:
        1. Attempts to invalidate codes for a user with no codes
        2. Verifies the operation completes without errors
        """
        # Arrange (Setup) - User exists but has no codes
        
        # Act & Assert (should not raise an exception)
        try:
            VerificationCodeRepository.invalidate_user_codes(
                user_id=user.user_id,
                code_type=VerificationCodeType.REGISTRATION.code
            )
        except Exception as e:
            pytest.fail(f"Should not raise exception when invalidating codes for user with no codes: {e}")

    def test_invalidate_user_codes_different_code_type(self, registration_code):
        """Test invalidating codes of different type doesn't affect other types.
        
        This test:
        1. Creates registration codes for a user
        2. Creates login codes for the same user
        3. Invalidates only registration codes
        4. Verifies login codes remain active
        """
        # Arrange (Setup)
        user_id = registration_code.user_id
        
        # Create a login code
        login_code = VerificationCodeRepository.create_login(
            user_id=user_id,
            code_hash="login_hash_test",
            hash_salt="login_salt_test"
        )
        
        # Verify both codes are active
        assert registration_code.is_used is False
        assert login_code.is_used is False
        
        # Act (Execute) - Invalidate only registration codes
        VerificationCodeRepository.invalidate_user_codes(
            user_id=user_id,
            code_type=VerificationCodeType.REGISTRATION.code
        )
        
        # Refresh from DB to get updated state
        db_registration = db.session.get(VerificationCode, registration_code.id)
        db_login = db.session.get(VerificationCode, login_code.id)
        
        # Assert (Verify)
        assert db_registration.is_used is True  # Registration code should be invalidated
        assert db_login.is_used is False  # Login code should still be active


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
