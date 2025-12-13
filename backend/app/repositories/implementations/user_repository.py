from typing import Optional, List
from app.models.user import User
from app import db
from app.models.verification_stutus_enum import VerificationStatusEnum
from app.repositories.base.user_repository_interface import (
    IUserRepository
)
from sqlalchemy.orm import joinedload


class UserRepository(IUserRepository):
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        return User.query.filter_by(email=email).first()
    
    def create_user(
        self,
        first_name: str,
        last_name: str,
        email: str,
        rotation_city_id: int
    ) -> User:
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            rotation_city_id=rotation_city_id,
            is_verified=False,
            status=VerificationStatusEnum.PENDING.code
        )
        db.session.add(new_user)
        db.session.commit()
        db.session.refresh(new_user)
        return new_user
    
    def mark_user_as_verified(self, user_id: int) -> Optional[User]:
        user: User = db.session.get(User, user_id)
        if user:
            user.is_verified = True
            user.status = VerificationStatusEnum.VERIFIED.code
            db.session.commit()
            db.session.refresh(user)
        return user
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return User.query.options(joinedload(User.rotation_city)).filter_by(user_id=user_id).first()
    
    def get_all_users(self) -> List[User]:
        return User.query.all()
    
    def update(self, user_id: int, **kwargs) -> User:
        user = db.session.get(User, user_id)
        if not user:
            raise ValueError("User not found")
        
        allowed_fields = ['first_name', 'last_name','rotation_city_id']

        for field in allowed_fields:
            if field in kwargs:
                setattr(user, field, kwargs[field])

        
        db.session.commit()
        db.session.refresh(user)
        return user
