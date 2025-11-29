from app.repositories.implementations.user_repository import UserRepository
from app.repositories.implementations.verification_code_repository import (
    VerificationCodeRepository
)
from app.services.auth.verification_code_service import (
    VerificationCodeService
)
from app.services.auth.notification_service import NotificationService
from app.models.user import User
from app.models.verification_code import VerificationCodeType
from flask import current_app


class LoginService:
    def __init__(
        self,
        user_repository: UserRepository = None,
        verification_code_repository: VerificationCodeRepository = None
    ):
        self.user_repo = user_repository or UserRepository()
        verification_repo = (
            verification_code_repository or VerificationCodeRepository()
        )
        self.verification_service = VerificationCodeService(
            verification_repo
        )
        self.notification_service = NotificationService()

    def initiate_login(self, email: str) -> None:
        """Send verification code to user for login."""
        user = self.user_repo.get_user_by_email(email)
        
        if not user:
            raise ValueError("User with this email does not exist.")
        
        if not user.is_verified:
            raise ValueError("User account is not verified. Please verify your email first.")
        
        # Development bypass for test user - skip sending code
        if current_app.config.get('DEBUG') and email == 'haya@uni.minerva.edu':
            return
        
        self.verification_service.repo.invalidate_user_codes(
            user_id=user.user_id,
            code_type=VerificationCodeType.LOGIN.code
        )
        
        verification_code, code = (
            self.verification_service.create_login_code(user)
        )
        
        self.notification_service.send_verification_code(
            user_email=user.email,
            name=user.first_name,
            verification_code=code,
            expiry_minutes=current_app.config[
                'VERIFICATION_CODE_EXPIRY_MINUTES'
            ]
        )

    def verify_login(self, email: str, verification_code: str) -> User:
        """Verify login code and return authenticated user."""
        user = self.user_repo.get_user_by_email(email)
        
        if not user:
            raise ValueError("User with this email does not exist.")
        
        if not user.is_verified:
            raise ValueError("User account is not verified.")
        
        # Development bypass for test user
        if current_app.config.get('DEBUG') and email == 'haya@uni.minerva.edu':
            return user
        
        is_code_valid = self.verification_service.verify_login_code(
            user=user,
            code=verification_code
        )
        
        if not is_code_valid:
            raise ValueError("Invalid or expired verification code.")
        
        return user
