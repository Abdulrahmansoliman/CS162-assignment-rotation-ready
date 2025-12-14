from datetime import datetime
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


class RateLimitExceededError(Exception):
    """Exception raised when verification code send rate limit is exceeded.
    
    Used to prevent abuse by limiting how many verification codes
    can be sent within a specific time window.
    """
    pass


class VerificationCodeService:
    """Service for verification code operations.
    
    Handles creation, validation, and lifecycle management of verification codes
    used for email verification during registration and login.
    """
    
    def __init__(
        self,
        verification_code_repository: VerificationCodeRepository = None
    ):
        """Initialize service with optional dependency injection.
        
        Args:
            verification_code_repository: Optional VerificationCodeRepository for testing/DI
        """
        self.repo = (
            verification_code_repository or VerificationCodeRepository()
        )
    
    def create_registration_code(self, user: User) -> VerificationCode:
        """Create a verification code for registration.
        
        Args:
            user: The User object to create the code for
            
        Returns:
            Tuple of (VerificationCode object, plain text code string)
            
        Raises:
            RateLimitExceededError: If rate limit is exceeded
        """
        # Check rate limit before creating new code
        self._check_rate_limit(user.user_id, VerificationCodeType.REGISTRATION.code)
        
        code = self._generate_code()
        code_hash, salt = self._hash_code(code)

        verification_code = self.repo.create_registration(
            user_id=user.user_id,
            code_hash=code_hash,
            hash_salt=salt
        )
        return verification_code, code
    
    def create_login_code(self, user: User) -> VerificationCode:
        """Create a verification code for login.
        
        Args:
            user: The User object to create the code for
            
        Returns:
            Tuple of (VerificationCode object, plain text code string)
            
        Raises:
            RateLimitExceededError: If rate limit is exceeded
        """
        # Check rate limit before creating new code
        self._check_rate_limit(user.user_id, VerificationCodeType.LOGIN.code)
        
        code = self._generate_code()
        code_hash, salt = self._hash_code(code)

        verification_code = self.repo.create_login(
            user_id=user.user_id,
            code_hash=code_hash,
            hash_salt=salt
        )
        return verification_code, code
    
    def verify_registration_code(self, user: User, code: str) -> bool:
        """Verify a registration verification code.
        
        Args:
            user: The User object to verify the code for
            code: The plain text verification code to validate
            
        Returns:
            True if code is valid, False otherwise
        """
        return self._verify_code(
            user=user,
            code=code,
            code_type=VerificationCodeType.REGISTRATION.code
        )
    
    def verify_login_code(self, user: User, code: str) -> bool:
        """Verify a login verification code.
        
        Args:
            user: The User object to verify the code for
            code: The plain text verification code to validate
            
        Returns:
            True if code is valid, False otherwise
        """
        return self._verify_code(
            user=user,
            code=code,
            code_type=VerificationCodeType.LOGIN.code
        )

    def _verify_code(self, user: User, code: str, code_type: str) -> bool:
        """Internal method to verify a code of any type.
        
        Args:
            user: The User object to verify the code for
            code: The plain text verification code to validate
            code_type: The type code from VerificationCodeType enum
            
        Returns:
            True if code is valid and not expired, False otherwise
        """
        verification_code: VerificationCode = (
            self.repo.find_most_recent_active_code(
                user_id=user.user_id,
                code_type=code_type
            )
        )
        
        if not verification_code:
            return False
        
        # check number of attempts
        if verification_code.attempts >= current_app.config.get('MAX_VERIFICATION_ATTEMPTS', 5):
            return False

        is_valid = self._validate_code(verification_code, code)
        if not is_valid:
            self.repo.increase_attempts(
                verification_code.verification_code_id
            )
            return False

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
    
    def _check_rate_limit(self, user_id: int, code_type: str) -> None:
        """Check if user has exceeded rate limit for sending codes."""
        max_codes = current_app.config.get('VERIFICATION_CODE_MAX_PER_HOUR', 3)
        time_window = current_app.config.get('VERIFICATION_CODE_RATE_LIMIT_WINDOW_MINUTES', 60)
        
        recent_codes = self.repo.get_recent_codes_time_window(
            user_id=user_id,
            code_type=code_type,
            since_minutes=time_window
        )
        
        remain_time = round(time_window - (
            datetime.utcnow() - recent_codes[-1].created_at
        ).total_seconds() / 60 if recent_codes else 0)

        if recent_codes and len(recent_codes) >= max_codes:
            raise RateLimitExceededError(
                f"Too many verification code requests. "
                f"Please wait {remain_time} minutes before requesting again."
            )
