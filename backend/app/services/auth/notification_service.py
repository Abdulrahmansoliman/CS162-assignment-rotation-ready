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