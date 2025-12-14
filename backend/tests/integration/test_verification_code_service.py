"""
Unit Tests for VerificationCodeService

Tests the code generation, hashing, and validation logic.
"""
import pytest
from datetime import datetime, timedelta
from app.services.auth.verification_code_service import VerificationCodeService
from app.models.verification_code import VerificationCode, VerificationCodeType
from app.repositories.implementations.verification_code_repository import (
    VerificationCodeRepository
)
from flask import current_app


@pytest.mark.integration
@pytest.mark.service
class TestVerificationCodeService:

    @pytest.fixture
    def service(self):
        return VerificationCodeService()

    @pytest.fixture
    def repository(self):
        return VerificationCodeRepository()

    def test_generate_code_has_correct_length_and_format(self, service, app_context):
        code = service._generate_code()
        assert isinstance(code, str)
        code_length = current_app.config.get('VERIFICATION_CODE_LENGTH', 6)
        assert len(code) == code_length
        allowed_chars = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        assert all(c in allowed_chars for c in code)

    def test_generate_code_produces_unique_codes(self, service):
        codes = [service._generate_code() for _ in range(10)]
        assert len(set(codes)) == len(codes)

    def test_hash_code_produces_valid_salted_sha256(self, service):
        code = "ABC123"
        code_hash, salt = service._hash_code(code)
        
        assert isinstance(code_hash, str)
        assert isinstance(salt, str)
        assert len(code_hash) == 64
        assert all(c in '0123456789abcdef' for c in code_hash)
        assert len(salt) > 0

    def test_hash_code_same_input_different_hashes_with_different_salts(self, service):
        code = "ABC123"
        hash1, salt1 = service._hash_code(code)
        hash2, salt2 = service._hash_code(code)
        assert hash1 != hash2
        assert salt1 != salt2

    def test_create_registration_code_persistence(
        self,
        service,
        user,
        db_session,
        app_context
    ):
        verification_code, code = service.create_registration_code(user)

        assert isinstance(verification_code, VerificationCode)
        assert isinstance(code, str)

        verification_code_db = db_session.get(
            VerificationCode, verification_code.verification_code_id
        )
        assert verification_code_db is not None
        assert verification_code_db.user_id == user.user_id
        assert verification_code_db.code_type == VerificationCodeType.REGISTRATION.code
        assert verification_code_db.is_used is False
        assert verification_code_db.attempts == 0
        assert verification_code_db.code_hash is not None
        assert verification_code_db.hash_salt is not None
        assert len(verification_code_db.code_hash) == 64
        assert code != verification_code_db.code_hash
        
        expected_len = current_app.config.get('VERIFICATION_CODE_LENGTH', 6)
        assert len(code) == expected_len

    # ============================================================================
    # Tests for verify_registration_code()
    # ============================================================================

    def test_verify_registration_code_valid_code_succeeds(
        self,
        service,
        user,
        db_session
    ):
        verification_code, code = service.create_registration_code(user)
        
        result = service.verify_registration_code(user, code)
        assert result is True
        
        code_db = db_session.get(VerificationCode, verification_code.verification_code_id)
        assert code_db.is_used is True

        active_code = service.repo.find_most_recent_active_code(
            user.user_id, VerificationCodeType.REGISTRATION.code
        )
        assert active_code is None

    def test_verify_registration_code_invalid_code_fails(
        self,
        service,
        user
    ):
        service.create_registration_code(user)
        result = service.verify_registration_code(user, "WRONGCODE")
        assert result is False

    def test_verify_registration_code_wrong_user_fails(
        self,
        service,
        user,
        unverified_user
    ):
        verification_code, code = service.create_registration_code(user)
        result = service.verify_registration_code(unverified_user, code)
        assert result is False

    def test_verify_registration_code_expired_code_fails(
        self,
        service,
        user,
        db_session,
        app_context
    ):
        code = service._generate_code()
        code_hash, salt = service._hash_code(code)

        now = datetime.utcnow()
        expired_code = VerificationCode(
            user_id=user.user_id,
            code_hash=code_hash,
            hash_salt=salt,
            code_type=VerificationCodeType.REGISTRATION.code,
            attempts=0,
            is_used=False,
            created_at=now - timedelta(minutes=20),
            expires_at=now - timedelta(minutes=5)
        )
        db_session.add(expired_code)
        db_session.commit()
        
        result = service.verify_registration_code(user, code)
        assert result is False

    def test_verify_registration_code_already_used_fails(
        self,
        service,
        user,
        db_session
    ):
        verification_code, code = service.create_registration_code(user)
        
        result1 = service.verify_registration_code(user, code)
        assert result1 is True
        
        verification_code_db = db_session.get(VerificationCode, verification_code.verification_code_id)
        assert verification_code_db.is_used is True

        result2 = service.verify_registration_code(user, code)
        assert result2 is False

    def test_verify_registration_code_max_attempts_fails(
        self,
        service,
        user,
        db_session,
        app_context
    ):
        max_attempts = current_app.config.get('MAX_VERIFICATION_ATTEMPTS', 5)
        verification_code, code = service.create_registration_code(user)

        for _ in range(max_attempts):
            service.verify_registration_code(user, "WRONGCODE")

        result = service.verify_registration_code(user, code)
        assert result is False

    def test_verify_registration_code_increments_attempts_on_failure(
        self,
        service,
        user,
        db_session
    ):
        verification_code, _ = service.create_registration_code(user)
        initial_attempts = verification_code.attempts
        
        service.verify_registration_code(user, "WRONGCODE")
        
        code_db = db_session.get(VerificationCode, verification_code.verification_code_id)
        assert code_db.attempts == initial_attempts + 1

    def test_verify_registration_code_marks_as_used_on_success(
        self,
        service,
        user,
        db_session
    ):
        verification_code, code = service.create_registration_code(user)
        service.verify_registration_code(user, code)
        code_db = db_session.get(VerificationCode, verification_code.verification_code_id)
        assert code_db.is_used is True

    def test_verify_registration_code_invalidates_other_codes(
        self,
        service,
        user,
        db_session
    ):
        code1_obj, code1 = service.create_registration_code(user)
        code2_obj, code2 = service.create_registration_code(user)
        code3_obj, code3 = service.create_registration_code(user)
        
        result = service.verify_registration_code(user, code3)
        assert result is True

        db_session.expire_all()
        code1_db = db_session.get(VerificationCode, code1_obj.verification_code_id)
        code2_db = db_session.get(VerificationCode, code2_obj.verification_code_id)
        
        assert code1_db.is_used is True
        assert code2_db.is_used is True

    def test_verify_login_code_valid_code_succeeds(
        self,
        service,
        verified_user,
        db_session
    ):
        verification_code, code = service.create_login_code(verified_user)
        result = service.verify_login_code(verified_user, code)
        assert result is True
        code_db = db_session.get(VerificationCode, verification_code.verification_code_id)
        assert code_db.is_used is True

    def test_verify_login_code_rejects_registration_code(
        self,
        service,
        verified_user,
        db_session
    ):
        verification_code, code = service.create_registration_code(verified_user)
        result = service.verify_login_code(verified_user, code)
        assert result is False

    def test_validate_code_correct_code_succeeds(
        self,
        service,
        user,
        db_session
    ):
        verification_code, plain_code = service.create_registration_code(user)
        result = service._validate_code(verification_code, plain_code)
        assert result is True

    def test_validate_code_incorrect_code_fails(
        self,
        service,
        user
    ):
        verification_code, _ = service.create_registration_code(user)
        result = service._validate_code(verification_code, "WRONGCODE")
        assert result is False

    def test_validate_code_requires_exact_match_and_case_sensitive(self, service, user):
        verification_code, plain_code = service.create_registration_code(user)
        
        assert service._validate_code(verification_code, plain_code.lower()) is False
        modified_code = plain_code[:-1] + ('A' if plain_code[-1] != 'A' else 'B')
        assert service._validate_code(verification_code, modified_code) is False

    def test_check_rate_limit_with_no_prior_requests(
        self,
        service,
        app_context,
        unverified_user
    ):
        service._check_rate_limit(
            user_id=unverified_user.user_id,
            code_type=VerificationCodeType.REGISTRATION.code,
        )  # Should not raise any exception