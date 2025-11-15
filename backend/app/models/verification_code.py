from app import db

class VerificationCode(db.Model):
    """Model for storing verification codes."""
    __tablename__ = 'verification_codes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    code_hash = db.Column(db.String(255), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    expires_at = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User', back_populates='verification_codes')

    def __repr__(self):
        return f"<VerificationCode(id={self.id}, user_id={self.user_id}, code_hash='{self.code_hash}')>"
    
    def is_expired(self):
        """Check if the verification code has expired."""
        return db.func.current_timestamp() > self.expires_at