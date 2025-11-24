import pytest
from datetime import datetime, timedelta
from app.repositories.implementations.verification_code_repository import (
    VerificationCodeRepository
)
from app.models.verification_code import VerificationCode, VerificationCodeType
from app import db


@pytest.mark.unit
@pytest.mark.repository
class TestVerificationCodeRepository:

    @pytest.fixture
    def repository(self):
        return VerificationCodeRepository()

    def test_create_registration_code_with_valid_data(
        self,
        db_session,
        repository,
        user
    ):
        code_hash = "test_hash_registration"
        hash_salt = "test_salt_registration"
        
        verification_code = repository.create_registration(
            user_id=user.user_id,
            code_hash=code_hash,
            hash_salt=hash_salt
        )
        
        assert verification_code is not None
        assert verification_code.verification_code_id is not None
        assert verification_code.user_id == user.user_id
        assert verification_code.code_hash == code_hash
        assert verification_code.hash_salt == hash_salt
        assert (
            verification_code.code_type ==
            VerificationCodeType.REGISTRATION.code
        )
        assert verification_code.is_used is False
        assert verification_code.attempts == 0

    def test_create_registration_code_sets_expiry_time(
        self,
        db_session,
        repository,
        user,
        app
    ):
        verification_code = repository.create_registration(
            user_id=user.user_id,
            code_hash="hash",
            hash_salt="salt"
        )
        
        expected_expiry = verification_code.created_at + timedelta(
            minutes=app.config.get('VERIFICATION_CODE_EXPIRY_MINUTES', 15)
        )
        
        assert verification_code.expires_at is not None
        assert abs(
            (verification_code.expires_at - expected_expiry).total_seconds()
        ) < 1

    def test_create_registration_code_persists_to_database(
        self,
        db_session,
        repository,
        user
    ):
        verification_code = repository.create_registration(
            user_id=user.user_id,
            code_hash="hash",
            hash_salt="salt"
        )
        
        db_session.expire_all()
        persisted = db_session.get(
            VerificationCode,
            verification_code.verification_code_id
        )
        
        assert persisted is not None
        assert persisted.user_id == user.user_id

    def test_create_login_code_with_valid_data(
        self,
        db_session,
        repository,
        user
    ):
        code_hash = "test_hash_login"
        hash_salt = "test_salt_login"
        
        verification_code = repository.create_login(
            user_id=user.user_id,
            code_hash=code_hash,
            hash_salt=hash_salt
        )
        
        assert verification_code is not None
        assert verification_code.verification_code_id is not None
        assert verification_code.code_type == VerificationCodeType.LOGIN.code
        assert verification_code.is_used is False

    def test_create_login_code_persists_to_database(
        self,
        db_session,
        repository,
        user
    ):
        verification_code = repository.create_login(
            user_id=user.user_id,
            code_hash="hash",
            hash_salt="salt"
        )
        
        db_session.expire_all()
        persisted = db_session.get(
            VerificationCode,
            verification_code.verification_code_id
        )
        
        assert persisted is not None
        assert persisted.code_type == VerificationCodeType.LOGIN.code

    def test_find_most_recent_active_code_returns_latest_valid_code(
        self,
        db_session,
        repository,
        user
    ):
        repository.create_registration(
            user_id=user.user_id,
            code_hash="older_hash",
            hash_salt="older_salt"
        )
        
        newer_code = repository.create_registration(
            user_id=user.user_id,
            code_hash="newer_hash",
            hash_salt="newer_salt"
        )
        
        result = repository.find_most_recent_active_code(
            user_id=user.user_id,
            code_type=VerificationCodeType.REGISTRATION.code
        )
        
        assert result is not None
        assert result.code_hash == newer_code.code_hash

    def test_find_most_recent_active_code_excludes_used_codes(
        self,
        db_session,
        repository,
        user
    ):
        used_code = repository.create_registration(
            user_id=user.user_id,
            code_hash="used_hash",
            hash_salt="used_salt"
        )
        used_code.is_used = True
        db_session.commit()
        
        result = repository.find_most_recent_active_code(
            user_id=user.user_id,
            code_type=VerificationCodeType.REGISTRATION.code
        )
        
        assert result is None

    def test_find_most_recent_active_code_excludes_expired_codes(
        self,
        db_session,
        repository,
        user
    ):
        expired_code = repository.create_registration(
            user_id=user.user_id,
            code_hash="expired_hash",
            hash_salt="expired_salt"
        )
        expired_code.expires_at = datetime.utcnow() - timedelta(hours=1)
        db_session.commit()
        
        result = repository.find_most_recent_active_code(
            user_id=user.user_id,
            code_type=VerificationCodeType.REGISTRATION.code
        )
        
        assert result is None

    def test_find_most_recent_active_code_filters_by_code_type(
        self,
        db_session,
        repository,
        user
    ):
        repository.create_registration(
            user_id=user.user_id,
            code_hash="reg_hash",
            hash_salt="reg_salt"
        )
        
        login_code = repository.create_login(
            user_id=user.user_id,
            code_hash="login_hash",
            hash_salt="login_salt"
        )
        
        result = repository.find_most_recent_active_code(
            user_id=user.user_id,
            code_type=VerificationCodeType.LOGIN.code
        )
        
        assert result is not None
        assert result.verification_code_id == login_code.verification_code_id

    def test_find_most_recent_active_code_returns_none_when_no_codes(
        self,
        db_session,
        repository,
        user
    ):
        result = repository.find_most_recent_active_code(
            user_id=user.user_id,
            code_type=VerificationCodeType.REGISTRATION.code
        )
        
        assert result is None

    def test_increase_attempts_increments_counter(
        self,
        db_session,
        repository,
        user
    ):
        code = repository.create_registration(
            user_id=user.user_id,
            code_hash="hash",
            hash_salt="salt"
        )
        
        initial_attempts = code.attempts
        repository.increase_attempts(code.verification_code_id)
        
        db_session.expire_all()
        updated_code = db_session.get(VerificationCode, code.verification_code_id)
        
        assert updated_code.attempts == initial_attempts + 1

    def test_increase_attempts_can_be_called_multiple_times(
        self,
        db_session,
        repository,
        user
    ):
        code = repository.create_registration(
            user_id=user.user_id,
            code_hash="hash",
            hash_salt="salt"
        )
        
        repository.increase_attempts(code.verification_code_id)
        repository.increase_attempts(code.verification_code_id)
        repository.increase_attempts(code.verification_code_id)
        
        db_session.expire_all()
        updated_code = db_session.get(VerificationCode, code.verification_code_id)
        
        assert updated_code.attempts == 3

    def test_increase_attempts_handles_nonexistent_code(
        self,
        db_session,
        repository
    ):
        repository.increase_attempts(99999)

    def test_mark_as_used_sets_is_used_flag(
        self,
        db_session,
        repository,
        user
    ):
        code = repository.create_registration(
            user_id=user.user_id,
            code_hash="hash",
            hash_salt="salt"
        )
        
        repository.mark_as_used(code.verification_code_id)
        
        db_session.expire_all()
        updated_code = db_session.get(VerificationCode, code.verification_code_id)
        
        assert updated_code.is_used is True
        assert updated_code.used_at is not None

    def test_mark_as_used_persists_changes(
        self,
        db_session,
        repository,
        user
    ):
        code = repository.create_registration(
            user_id=user.user_id,
            code_hash="hash",
            hash_salt="salt"
        )
        
        repository.mark_as_used(code.verification_code_id)
        
        db_session.expire_all()
        persisted = db_session.get(VerificationCode, code.verification_code_id)
        
        assert persisted.is_used is True

    def test_mark_as_used_handles_nonexistent_code(
        self,
        db_session,
        repository
    ):
        repository.mark_as_used(99999)

    def test_invalidate_user_codes_marks_all_active_codes_as_used(
        self,
        db_session,
        repository,
        user
    ):
        code1 = repository.create_registration(
            user_id=user.user_id,
            code_hash="hash1",
            hash_salt="salt1"
        )
        code2 = repository.create_registration(
            user_id=user.user_id,
            code_hash="hash2",
            hash_salt="salt2"
        )
        
        repository.invalidate_user_codes(
            user_id=user.user_id,
            code_type=VerificationCodeType.REGISTRATION.code
        )
        
        db_session.expire_all()
        updated_code1 = db_session.get(VerificationCode, code1.verification_code_id)
        updated_code2 = db_session.get(VerificationCode, code2.verification_code_id)
        
        assert updated_code1.is_used is True
        assert updated_code2.is_used is True

    def test_invalidate_user_codes_filters_by_code_type(
        self,
        db_session,
        repository,
        user
    ):
        reg_code = repository.create_registration(
            user_id=user.user_id,
            code_hash="reg_hash",
            hash_salt="reg_salt"
        )
        login_code = repository.create_login(
            user_id=user.user_id,
            code_hash="login_hash",
            hash_salt="login_salt"
        )
        
        repository.invalidate_user_codes(
            user_id=user.user_id,
            code_type=VerificationCodeType.REGISTRATION.code
        )
        
        db_session.expire_all()
        updated_reg = db_session.get(VerificationCode, reg_code.verification_code_id)
        updated_login = db_session.get(VerificationCode, login_code.verification_code_id)
        
        assert updated_reg.is_used is True
        assert updated_login.is_used is False

    def test_invalidate_user_codes_does_not_affect_already_used_codes(
        self,
        db_session,
        repository,
        user
    ):
        code = repository.create_registration(
            user_id=user.user_id,
            code_hash="hash",
            hash_salt="salt"
        )
        code.is_used = True
        code.used_at = datetime.utcnow()
        db_session.commit()
        original_used_at = code.used_at
        
        repository.invalidate_user_codes(
            user_id=user.user_id,
            code_type=VerificationCodeType.REGISTRATION.code
        )
        
        db_session.expire_all()
        updated_code = db_session.get(VerificationCode, code.verification_code_id)
        
        assert updated_code.is_used is True

    def test_invalidate_user_codes_does_not_affect_expired_codes(
        self,
        db_session,
        repository,
        user
    ):
        code = repository.create_registration(
            user_id=user.user_id,
            code_hash="hash",
            hash_salt="salt"
        )
        code.expires_at = datetime.utcnow() - timedelta(hours=1)
        db_session.commit()
        
        repository.invalidate_user_codes(
            user_id=user.user_id,
            code_type=VerificationCodeType.REGISTRATION.code
        )
        
        db_session.expire_all()
        updated_code = db_session.get(VerificationCode, code.verification_code_id)
        
        assert updated_code.is_used is False

    def test_invalidate_user_codes_handles_no_matching_codes(
        self,
        db_session,
        repository,
        user
    ):
        repository.invalidate_user_codes(
            user_id=user.user_id,
            code_type=VerificationCodeType.REGISTRATION.code
        )
