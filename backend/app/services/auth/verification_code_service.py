from app.models.verification_code import VerificationCode, VerificationCodeType
from app.repositories.implementations.verification_code_repository import (
    VerificationCodeRepository
)
from app.models.user import User
import os
from flask import current_app
import random
import string
import hashlib


class VerificationCodeService:
    def __init__(
        self,
        verification_code_repository: VerificationCodeRepository = None
    ):
        self.repo = (
            verification_code_repository or VerificationCodeRepository()
        )
    
    def create_registration_code(self, user: User) -> VerificationCode:
        code = self._generate_code()
        code_hash, salt = self._hash_code(code)

        verification_code = self.repo.create_registration(
            user_id=user.user_id,
            code_hash=code_hash,
            hash_salt=salt
        )
        return verification_code, code

    def verify_registration_code(self, user: User, code: str) -> bool:
        return self._verify_code(
            user=user,
            code=code,
            code_type=VerificationCodeType.REGISTRATION.code
        )

    def verify_login_code(self, user: User, code: str) -> bool:
        return self._verify_code(
            user=user,
            code=code,
            code_type=VerificationCodeType.LOGIN.code
        )

    def _verify_code(self, user: User, code: str, code_type: str) -> bool:
        verification_code: VerificationCode = (
            self.repo.find_most_recent_active_code(
                user_id=user.user_id,
                code_type=code_type
            )
        )

        if not verification_code:
            return False

        is_valid = self._validate_code(verification_code, code)
        if not is_valid:
            self.repo.increase_attempts(
                verification_code.verification_code_id
            )
            return False

        # Mark code as used
        self.repo.mark_as_used(verification_code.verification_code_id)

        self.repo.invalidate_user_codes(
            user_id=user.user_id,
            code_type=code_type
        )

        return True

    def _validate_code(
        self,
        verification_code: VerificationCode,
        code: str
    ) -> bool:
        hash_input = (
            f"{code}{verification_code.hash_salt}"
            f"{current_app.config['SECRET_KEY']}"
        ).encode('utf-8')
        code_hash = hashlib.sha256(hash_input).hexdigest()
        return code_hash == verification_code.code_hash

    def _hash_code(self, code: str) -> str:
        salt = os.urandom(16).hex()
        hash_input = (
            f"{code}{salt}{current_app.config['SECRET_KEY']}"
        ).encode('utf-8')
        code_hash = hashlib.sha256(hash_input).hexdigest()

        return code_hash, salt

    def _generate_code(self) -> str:
        code_length = current_app.config.get('VERIFICATION_CODE_LENGTH', 6)
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choice(characters) for _ in range(code_length))
