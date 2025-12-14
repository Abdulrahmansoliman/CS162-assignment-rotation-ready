import enum

class VerificationStatusEnum(enum.Enum):
    """Enumeration for user verification status.
    
    Tracks the email verification state of user accounts.
    Uses integer codes for database storage with descriptive labels.
    
    Members:
        PENDING (0): User registered but email not verified yet
        VERIFIED (1): User email successfully verified
        EXPIRED (2): Verification period expired
    """
    PENDING = (0, "Pending Verification")
    VERIFIED = (1, "Verified User")
    EXPIRED = (2, "Verification Expired")

    def __init__(self, code, description):
        self.code = code
        self.description = description
    
    @classmethod
    def from_code(cls, code):
        """Get enum member from code value.
        
        Args:
            code (int): The integer code (0, 1, or 2)
            
        Returns:
            VerificationStatusEnum: The matching enum member
            
        Raises:
            ValueError: If code doesn't match any member
        """
        for status in cls:
            if status.code == code:
                return status
        raise ValueError(f"No VerificationStatusEnum with code {code}")

    
