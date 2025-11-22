from typing import Optional
from app.models.user import User
from app import db
from backend.app.models.verification_status_enum import VerificationStatusEnum

class UserRepository:
    @staticmethod
    def get_user_by_email(email: str) -> Optional[User]:
        """Retrieve a user by their email address."""
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def create_user(first_name: str, last_name: str, email: str, rotation_city_id: int) -> User:
        """Create a new user in the database."""
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
    
    @staticmethod
    def mark_user_as_verified(user_id: int) -> Optional[User]:
        """Mark a user as verified."""
        user: User = User.query.get(user_id)
        if user:
            user.is_verified = True
            user.status = VerificationStatusEnum.VERIFIED.code
            db.session.commit()
        return user
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        """Retrieve a user by their ID."""
        return User.query.get(user_id)
    
    @staticmethod
    def get_all_users() -> list[User]:
        """Retrieve all users from the database."""
        return User.query.all()   

    @staticmethod
    def update(user_id: User, **kwargs) -> User:
        """Update user attributes."""
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found.")
        
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)

        db.session.commit()
        db.session.refresh(user)
        return user
        