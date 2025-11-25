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


class RegistrationService:
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
    
    def register_user(
        self,
        first_name: str,
        last_name: str,
        email: str,
        rotation_city_id: int
    ) -> User:
        """Registers a new user in the system."""
        # Check if user already exists
        existing_user = self.user_repo.get_user_by_email(email)
        if existing_user:
            if existing_user.is_verified:
                raise ValueError(
                    "User with this email already exists. Login instead."
                )
            else:
                # Handle expired unverified user
                self._handle_expired_user(
                    existing_user,
                    {
                        'first_name': first_name,
                        'last_name': last_name,
                        'rotation_city_id': rotation_city_id
                    })
                return None  # Indicate that verification code should be resent
        
        # Create new user
        new_user = self.user_repo.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            rotation_city_id=rotation_city_id
        )

        # generate and send verification code logic can be added here
        verification_code, code = (
            self.verification_service.create_registration_code(new_user)
        )

        # Send the verification code to the user's email
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
        # Update user information
        self.user_repo.update(user.user_id, **updates)

        # Logic to resend verification code can be added here
        verification_code, code = (
            self.verification_service.create_registration_code(user)
        )

        # Send the verification code to the user's email
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

        # Verify the code
        is_code_valid = self.verification_service.verify_registration_code(
            user=user,
            code=verification_code
        )

        if not is_code_valid:
            raise ValueError("Invalid or expired verification code.")

        # Mark user as verified
        self.user_repo.mark_user_as_verified(user.user_id)

        return user
