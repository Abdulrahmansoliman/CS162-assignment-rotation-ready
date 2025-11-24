from app import db
from enum import Enum

class VerificationCodeType(Enum):
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
    """Model for storing verification codes."""
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

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    expires_at = db.Column(db.DateTime, nullable=False)
    used_at = db.Column(db.DateTime, nullable=True)

    user = db.relationship('User', back_populates='verification_codes')

    def __repr__(self):
        return f"<VerificationCode(verification_code_id={self.verification_code_id}, user_id={self.user_id}, code_hash='{self.code_hash}')>"
    
    def is_expired(self):
        """Check if the verification code has expired."""
        return db.func.current_timestamp() > self.expires_at