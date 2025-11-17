from app import db
from enum import Enum

class VerificationCodeType(Enum):
    REGISTRATION = (0, 'registration')
    LOGIN = (1, 'login')

    def __init__(self, value, name):
        self._value_ = value
        self.name = name

class VerificationCode(db.Model):
    """Model for storing verification codes."""
    __tablename__ = 'verification_code'

    id = db.Column(db.Integer, primary_key=True)
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
        return f"<VerificationCode(id={self.id}, user_id={self.user_id}, code_hash='{self.code_hash}')>"
    
    def is_expired(self):
        """Check if the verification code has expired."""
        return db.func.current_timestamp() > self.expires_at