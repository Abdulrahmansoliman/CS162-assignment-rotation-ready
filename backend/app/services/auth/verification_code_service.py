from app.models.verification_code import VerificationCode, VerificationCodeType
from app.repositories.verification_code_repository import VerificationCodeRepository
from app.models.user import User
import os
from flask import current_app
import random
import string
import hashlib
from app import db

class VerificationCodeService:
    @staticmethod
    def create_registration_code(user: User, ) -> VerificationCode:
        """Create a new registration code for a user."""
        code = VerificationCodeService._generate_code()
        code_hash, salt = VerificationCodeService._hash_code(code)

        verification_code = VerificationCodeRepository.create_registration(
            user_id=user.user_id,
            code_hash=code_hash,
            hash_salt=salt
        )
        return verification_code, code  # Return both the object and the plain code
    
    @staticmethod
    def verify_registration_code(user: User, code: str) -> bool:
        """Verify a registration code for a user."""
        return VerificationCodeService._verify_code(
            user=user,
            code=code,
            code_type=VerificationCodeType.REGISTRATION.code
        )
    
    @staticmethod
    def verify_login_code(user: User, code: str) -> bool:
        """Verify a login code for a user."""
        return VerificationCodeService._verify_code(
            user=user,
            code=code,
            code_type=VerificationCodeType.LOGIN.code
        )

    @staticmethod
    def _verify_code(user: User, code: str, code_type: str) -> bool:
        """Verify a given code for a user and code type."""
        verification_code: VerificationCode =\
            VerificationCodeRepository.find_most_recent_active_code(
                user_id=user.user_id,
                code_type=code_type
            )
        
        if not verification_code:
            return False
        
        is_valid = VerificationCodeService._validate_code(verification_code, code)
        if not is_valid:
            VerificationCodeRepository.increase_attempts(verification_code.verification_code_id)
            return False

        # Mark code as used
        VerificationCodeRepository.mark_code_as_used(
            verification_code.verification_code_id
        )

        VerificationCodeRepository.invalidate_user_codes(
            user_id=user.user_id,
            code_type=code_type
        )

        return True

    @staticmethod
    def _validate_code(verification_code: VerificationCode, code: str) -> bool:
        """Validate the provided code against the stored hash."""
        hash_input = f"{code}{verification_code.hash_salt}{current_app.config['SECRET_KEY']}".encode('utf-8')
        code_hash = hashlib.sha256(hash_input).hexdigest()
        return code_hash == verification_code.code_hash        
    
    @staticmethod
    def _hash_code(code: str) -> str:
        """Hash the verification code."""
        salt = os.urandom(16).hex()
        hash_input = f"{code}{salt}{current_app.config['SECRET_KEY']}".encode('utf-8')
        code_hash = hashlib.sha256(hash_input).hexdigest()

        return code_hash, salt

    @staticmethod
    def _generate_code() -> str:
        """Generate a random verification code."""
        code_length = current_app.config.get('VERIFICATION_CODE_LENGTH', 6)
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choice(characters) for _ in range(code_length))