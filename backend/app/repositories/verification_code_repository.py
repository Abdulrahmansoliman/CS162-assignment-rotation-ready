from app.models.verification_code import VerificationCode, VerificationCodeType
from app import db
from datetime import datetime, timedelta
from flask import current_app

class VerificationCodeRepository:
    @staticmethod
    def create_registration(**kwargs) -> VerificationCode:
        """Create a new registration verification code for a user."""
        return VerificationCodeRepository._create_code(
            user_id=kwargs.get("user_id"),
            code_hash=kwargs.get("code_hash"),
            hash_salt=kwargs.get("hash_salt"),
            code_type=VerificationCodeType.REGISTRATION.code
        )
    
    @staticmethod
    def create_login(**kwargs) -> VerificationCode:
        """Create a new login verification code for a user."""
        return VerificationCodeRepository._create_code(
            user_id=kwargs.get("user_id"),
            code_hash=kwargs.get("code_hash"),
            hash_salt=kwargs.get("hash_salt"),
            code_type=VerificationCodeType.LOGIN.code
        )

    @staticmethod
    def _create_code(**kwargs) -> VerificationCode:
        """Create a new verification code of a specified type for a user."""
        now = datetime.utcnow()
        expiry_minutes = current_app.config.get('VERIFICATION_CODE_EXPIRY_MINUTES', 15)
        
        new_code = VerificationCode(
            user_id=kwargs.get("user_id"),
            code_hash=kwargs.get("code_hash"),
            hash_salt=kwargs.get("hash_salt"),
            code_type=kwargs.get("code_type"),
            created_at=now,
            expires_at=now + timedelta(minutes=expiry_minutes)
        )
        db.session.add(new_code)
        db.session.commit()
        return new_code
    
    def find_most_recent_active_code(user_id: int, code_type: str) -> VerificationCode:
        """
        Find active """
        return VerificationCode.query.filter(
            VerificationCode.user_id == user_id,
            VerificationCode.code_type == code_type,
            VerificationCode.is_used == False,
            VerificationCode.expires_at > db.func.current_timestamp()
        ).order_by(
            VerificationCode.created_at.desc()
        ).first()
    
    def increase_attempts(verification_code_id: int) -> None:
        """Increase the attempt count for a verification code."""
        code: VerificationCode = VerificationCode.query.get(verification_code_id)
        if code:
            code.attempts += 1
            db.session.commit()
            db.session.refresh(code)


    def mark_code_as_used(verification_code_id: int) -> None:
        """Mark a verification code as used."""
        code: VerificationCode = VerificationCode.query.get(verification_code_id)
        if code:
            code.is_used = True
            code.used_at = db.func.current_timestamp()
            db.session.commit()
            db.session.refresh(code)
        
    def invalidate_user_codes(user_id, code_type):
        """Invalidate all active codes for a user and code type."""
        db.session.query(VerificationCode).filter(
            VerificationCode.user_id == user_id,
            VerificationCode.code_type == code_type,
            VerificationCode.is_used == False,
            VerificationCode.expires_at > db.func.current_timestamp()
        ).update({
            VerificationCode.is_used: True,
            VerificationCode.used_at: db.func.current_timestamp()
        })
        db.session.commit()


    
