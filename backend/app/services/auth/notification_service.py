class NotificationService:
    @staticmethod
    def send_verification_code(
        user_email: str,
        name: str,
        verification_code: str,
        expiry_minutes: int
    ) -> None:
        """Send a verification code to the user's email."""
        # Email sending logic goes here
        print(f"Sending verification code {verification_code} to {user_email}. It expires in {expiry_minutes} minutes.")
    
    @staticmethod
    def send_password_reset_email(
        user_email: str,
        name: str,
        reset_url: str,
        expiry_minutes: int
    ) -> None:
        """Send a password reset link to the user's email."""
        # Email sending logic goes here
        print(f"Sending password reset link to {user_email}:")
        print(f"Hello {name}, click this link to reset your password: {reset_url}")
        print(f"This link expires in {expiry_minutes} minutes.")