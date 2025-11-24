from app.repositories.implementations.user_repository import UserRepository
from app.repositories.implementations.verification_code_repository import (
    VerificationCodeRepository
)
from app.services.auth.verification_code_service import (
    VerificationCodeService
)
from app.services.auth.notification_service import NotificationService
from app.models.user import User
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
