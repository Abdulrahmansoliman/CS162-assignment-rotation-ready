from typing import Optional
from datetime import datetime, timedelta
from flask import current_app
from app.models.verification_code import VerificationCode, VerificationCodeType
from app import db
from app.repositories.base.verification_code_repository_interface import (
    IVerificationCodeRepository
)


class VerificationCodeRepository(IVerificationCodeRepository):
    
    def create_registration(self, **kwargs) -> VerificationCode:
        return self._create_code(
            user_id=kwargs.get("user_id"),
            code_hash=kwargs.get("code_hash"),
            hash_salt=kwargs.get("hash_salt"),
            code_type=VerificationCodeType.REGISTRATION.code
        )
    
    def create_login(self, **kwargs) -> VerificationCode:
        return self._create_code(
            user_id=kwargs.get("user_id"),
            code_hash=kwargs.get("code_hash"),
            hash_salt=kwargs.get("hash_salt"),
            code_type=VerificationCodeType.LOGIN.code
        )

    def _create_code(self, **kwargs) -> VerificationCode:
        now = datetime.utcnow()
        expiry_minutes = current_app.config.get(
            'VERIFICATION_CODE_EXPIRY_MINUTES',
            15
        )
        
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
        db.session.refresh(new_code)
        return new_code
    
    def find_most_recent_active_code(
        self,
        user_id: int,
        code_type: str
    ) -> Optional[VerificationCode]:
        return VerificationCode.query.filter(
            VerificationCode.user_id == user_id,
            VerificationCode.code_type == code_type,
            VerificationCode.is_used.is_(False),
            VerificationCode.expires_at > db.func.current_timestamp()
        ).order_by(
            VerificationCode.created_at.desc(),
            VerificationCode.verification_code_id.desc()
        ).first()
    
    def increase_attempts(self, verification_code_id: int) -> None:
        code: VerificationCode = db.session.get(
            VerificationCode,
            verification_code_id
        )
        if code:
            code.attempts += 1
            db.session.commit()
            db.session.refresh(code)

    def mark_as_used(self, verification_code_id: int) -> None:
        code: VerificationCode = db.session.get(
            VerificationCode,
            verification_code_id
        )
        if code:
            code.is_used = True
            code.used_at = db.func.current_timestamp()
            db.session.commit()
            db.session.refresh(code)
    
    def invalidate_user_codes(self, user_id: int, code_type: str) -> None:
        db.session.query(VerificationCode).filter(
            VerificationCode.user_id == user_id,
            VerificationCode.code_type == code_type,
            VerificationCode.is_used.is_(False),
            VerificationCode.expires_at > db.func.current_timestamp()
        ).update({
            VerificationCode.is_used: True,
            VerificationCode.used_at: db.func.current_timestamp()
        })
        db.session.commit()
    
    def count_recent_codes(
        self,
        user_id: int,
        code_type: str,
        since_minutes: int
    ) -> int:
        """Count verification codes sent within the last N minutes."""
        time_threshold = datetime.utcnow() - timedelta(minutes=since_minutes)
        
        count = db.session.query(VerificationCode).filter(
            VerificationCode.user_id == user_id,
            VerificationCode.code_type == code_type,
            VerificationCode.sent_at >= time_threshold
        ).count()
        
        return count
