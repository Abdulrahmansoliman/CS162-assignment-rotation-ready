import enum

class VerificationStatusEnum(enum.Enum):
    """Enumeration for user verification status."""
    PENDING = (0, "Pending Verification")
    VERIFIED = (1, "Verified User")
    EXPIRED = (2, "Verification Expired")

    def __init__(self, code, description):
        self.code = code
        self.description = description
    
    @classmethod
    def from_code(cls, code):
        """Get enum member by code."""
        for status in cls:
            if status.code == code:
                return status
        raise ValueError(f"No VerificationStatusEnum with code {code}")

    
