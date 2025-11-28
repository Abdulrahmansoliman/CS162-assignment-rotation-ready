from app.repositories.implementations.user_repository import UserRepository
from app.repositories.implementations.verification_code_repository import (
    VerificationCodeRepository
)
from app.services.auth.verification_code_service import (
    VerificationCodeService
)
from backend.app.repositories.implementations.rotation_city_repository import (
    RotationCityRepository
)
from app.services.auth.notification_service import NotificationService
from app.models.user import User
from flask import current_app



class RegistrationService:
    def __init__(
        self,
        user_repository: UserRepository = None,
        verification_code_repository: VerificationCodeRepository = None,
        rotation_city_repository: RotationCityRepository = None
    ):
        self.user_repo = user_repository or UserRepository()
        verification_repo = (
            verification_code_repository or VerificationCodeRepository()
        )
        self.rotation_city_repo = (
            rotation_city_repository or RotationCityRepository()
        )
        self.verification_service = VerificationCodeService(
            verification_repo
        )
        self.notification_service = NotificationService()
    
    def register_user(
        self,
        first_name: str,
        last_name: str,
        email: str,
        rotation_city_id: int
    ) -> User:
        """Registers a new user in the system."""
        existing_user = self.user_repo.get_user_by_email(email)

        # validate rotation_city_id
        rotation_city_id = self.rotation_city_repo.validate_city_id(rotation_city_id)

        if existing_user:
            if existing_user.is_verified:
                raise ValueError(
                    "User with this email already exists. Login instead."
                )
            else:
                self._handle_expired_user(
                    existing_user,
                    {
                        'first_name': first_name,
                        'last_name': last_name,
                        'rotation_city_id': rotation_city_id
                    }
                )
                return None
        
        new_user = self.user_repo.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            rotation_city_id=rotation_city_id
        )

        verification_code, code = (
            self.verification_service.create_registration_code(new_user)
        )

        self.notification_service.send_verification_code(
            user_email=new_user.email,
            name=new_user.first_name,
            verification_code=code,
            expiry_minutes=current_app.config[
                'VERIFICATION_CODE_EXPIRY_MINUTES'
            ]
        )

        return new_user

    def _handle_expired_user(self, user: User, updates: dict):
        """Handle logic for expired unverified users."""
        self.user_repo.update(user.user_id, **updates)

        verification_code, code = (
            self.verification_service.create_registration_code(user)
        )

        self.notification_service.send_verification_code(
            user_email=user.email,
            name=user.first_name,
            verification_code=code,
            expiry_minutes=current_app.config[
                'VERIFICATION_CODE_EXPIRY_MINUTES'
            ]
        )

        return user
    
    def verify_user_email(self, email: str, verification_code: str) -> User:
        user = self.user_repo.get_user_by_email(email)

        if not user:
            raise ValueError("User with this email does not exist.")
        
        if user.is_verified:
            raise ValueError("User is already verified. Please log in.")
        
        is_code_valid = self.verification_service.verify_registration_code(
            user=user,
            code=verification_code
        )

        if not is_code_valid:
            raise ValueError("Invalid or expired verification code.")

        self.user_repo.mark_user_as_verified(user.user_id)

        return user

    def resend_verification_code(self, email: str) -> None:
        """Resend verification code to user email."""
        user = self.user_repo.get_user_by_email(email)

        if not user:
            raise ValueError("User with this email does not exist.")
        
        if user.is_verified:
            raise ValueError("User is already verified. Please log in.")

        verification_code, code = (
            self.verification_service.create_registration_code(user)
        )

        self.notification_service.send_verification_code(
            user_email=user.email,
            name=user.first_name,
            verification_code=code,
            expiry_minutes=current_app.config[
                'VERIFICATION_CODE_EXPIRY_MINUTES'
            ]
        )
