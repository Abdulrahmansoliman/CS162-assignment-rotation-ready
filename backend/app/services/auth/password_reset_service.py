import secrets
from typing import Optional
from flask import current_app
from app.models.user import User
from app.models.verification_code import VerificationCodeType
from app.repositories.implementations.user_repository import UserRepository
from app.repositories.implementations.verification_code_repository import (
    VerificationCodeRepository
)
from app.services.auth.notification_service import NotificationService


class PasswordResetError(Exception):
    """Base exception for password reset errors."""
    pass


class InvalidOrExpiredTokenError(PasswordResetError):
    """Raised when a reset token is invalid or expired."""
    pass


class PasswordResetService:
    def __init__(
        self,
        user_repository: UserRepository = None,
        verification_code_repository: VerificationCodeRepository = None,
        notification_service: NotificationService = None
    ):
        self.user_repo = user_repository or UserRepository()
        self.verification_repo = (
            verification_code_repository or VerificationCodeRepository()
        )
        self.notification_service = (
            notification_service or NotificationService()
        )
    
    def request_reset(self, email: str) -> None:
        """
        Initiate password reset for a user.
        Returns silently if user doesn't exist to prevent email enumeration.
        """
        user = self.user_repo.get_user_by_email(email)
        if not user:
            # Return without error to avoid user enumeration
            return
        
        # Invalidate any existing password reset codes for this user
        self.verification_repo.invalidate_user_codes(
            user_id=user.user_id,
            code_type=VerificationCodeType.PASSWORD_RESET.code
        )
        
        # Generate new reset token
        raw_token = secrets.token_urlsafe(32)
        token_hash, salt = self._hash_token(raw_token)
        
        # Create password reset code
        self.verification_repo.create_password_reset(
            user_id=user.user_id,
            code_hash=token_hash,
            hash_salt=salt
        )
        
        # Send reset email
        reset_url = self._build_reset_url(raw_token)
        self.notification_service.send_password_reset_email(
            user_email=user.email,
            name=user.first_name,
            reset_url=reset_url,
            expiry_minutes=current_app.config.get(
                'VERIFICATION_CODE_EXPIRY_MINUTES',
                15
            )
        )
    
    def confirm_reset(self, token: str, new_password: str) -> None:
        """
        Confirm password reset with token and set new password.
        Raises InvalidOrExpiredTokenError if token is invalid.
        """
        # Find valid password reset code by checking token against all active codes
        reset_code = self._find_valid_reset_code(token)
        if not reset_code:
            raise InvalidOrExpiredTokenError(
                "Invalid or expired reset token"
            )
        
        # Update user password
        self.user_repo.update_password(
            user_id=reset_code.user_id,
            new_password=new_password
        )
        
        # Mark code as used
        self.verification_repo.mark_as_used(
            reset_code.verification_code_id
        )
    
    def _find_valid_reset_code(self, token: str):
        """Find a valid password reset code by validating token with each salt."""
        from app.models.verification_code import VerificationCode
        from app import db
        import hashlib
        
        active_codes = VerificationCode.query.filter(
            VerificationCode.code_type == (
                VerificationCodeType.PASSWORD_RESET.code
            ),
            VerificationCode.is_used.is_(False),
            VerificationCode.expires_at > db.func.current_timestamp()
        ).all()
        
        # Check each active code's hash with its salt
        for code in active_codes:
            hash_input = (
                f"{token}{code.hash_salt}{current_app.config['SECRET_KEY']}"
            ).encode('utf-8')
            computed_hash = hashlib.sha256(hash_input).hexdigest()
            
            if computed_hash == code.code_hash:
                return code
        
        return None
    
    def _validate_token_hash(self, token_hash: str, code) -> bool:
        """Check if the provided token hash matches the stored code."""
        return token_hash == code.code_hash
    
    def _hash_token(self, token: str) -> tuple:
        """Hash a token with a new salt."""
        import os
        import hashlib
        
        salt = os.urandom(16).hex()
        hash_input = (
            f"{token}{salt}{current_app.config['SECRET_KEY']}"
        ).encode('utf-8')
        token_hash = hashlib.sha256(hash_input).hexdigest()
        
        return token_hash, salt
    
    def _build_reset_url(self, token: str) -> str:
        """Build the password reset URL for the frontend."""
        frontend_url = current_app.config.get(
            'FRONTEND_URL',
            'http://localhost:5173'
        )
        return f"{frontend_url}/reset-password?token={token}"
