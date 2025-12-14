from app import db
from enum import Enum

class VerificationCodeType(Enum):
    """Enum for verification code types.
    
    Defines the purpose of verification codes sent to users.
    
    Members:
        REGISTRATION (0, 'registration'): Email verification during signup
        LOGIN (1, 'login'): Passwordless login verification
    """
    REGISTRATION = (0, "registration")
    LOGIN = (1, "login")

    def __init__(self, code, label):
        self._code = code
        self._label = label

    @property
    def code(self):
        return self._code

    @property
    def label(self):
        return self._label

class VerificationCode(db.Model):
    """Model for storing verification codes for email verification.
    
    Stores hashed 6-digit codes sent to users for registration and login.
    Includes security features like attempt tracking and expiration.
    
    Attributes:
        verification_code_id (int): Primary key, auto-incrementing
        user_id (int): Foreign key to user (indexed)
        code_hash (str): Unique hashed verification code (max 255 chars)
        hash_salt (str): Salt used for hashing (max 255 chars)
        code_type (int): Type code from VerificationCodeType enum
        attempts (int): Number of failed verification attempts
        is_used (bool): Whether code has been successfully used (indexed)
        created_at (datetime): Code creation timestamp (indexed)
        expires_at (datetime): Code expiration timestamp
        used_at (datetime): When code was successfully used
        user: Relationship to User model
    """
    __tablename__ = 'verification_code'

    verification_code_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False, index=True)

    # Code information
    code_hash = db.Column(db.String(255), nullable=False, unique=True)
    hash_salt = db.Column(db.String(255), nullable=False)
    code_type = db.Column(
        db.Integer,
        nullable=False
    )  # Use VerificationCodeType enum values

    # Security tracking
    attempts = db.Column(db.Integer, default=0, nullable=False)
    is_used = db.Column(db.Boolean, default=False, nullable=False, index=True)

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False, index=True)
    expires_at = db.Column(db.DateTime, nullable=False)
    used_at = db.Column(db.DateTime, nullable=True)

    user = db.relationship('User', back_populates='verification_codes')

    def __repr__(self):
        """Return string representation of VerificationCode instance."""
        return f"<VerificationCode(verification_code_id={self.verification_code_id}, user_id={self.user_id}, code_hash='{self.code_hash}')>"
    
    def is_expired(self):
        """Check if the verification code has expired.
        
        Returns:
            bool: True if current time is past expires_at, False otherwise
        """
        return db.func.current_timestamp() > self.expires_at