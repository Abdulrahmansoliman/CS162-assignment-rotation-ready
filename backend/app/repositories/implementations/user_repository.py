from typing import Optional, List
from app.models.user import User
from app import db
from app.models.verification_stutus_enum import VerificationStatusEnum
from app.repositories.base.user_repository_interface import (
    IUserRepository
)
from sqlalchemy.orm import joinedload


class UserRepository(IUserRepository):
    """Repository for user data access operations.
    
    Handles all database operations related to users including
    creation, retrieval, updates, and verification status changes.
    """
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by their email address.
        
        Args:
            email: The email address to search for
            
        Returns:
            User object if found, None otherwise
        """
        return User.query.filter_by(email=email).first()
    
    def create_user(
        self,
        first_name: str,
        last_name: str,
        email: str,
        rotation_city_id: int
    ) -> User:
        """Create a new user in the database.
        
        Args:
            first_name: User's first name
            last_name: User's last name
            email: User's email address
            rotation_city_id: ID of the user's rotation city
            
        Returns:
            Created User object with status set to PENDING
        """
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
        """Mark a user as verified in the database.
        
        Args:
            user_id: The ID of the user to verify
            
        Returns:
            Updated User object if found, None otherwise
        """
        user: User = db.session.get(User, user_id)
        if user:
            user.is_verified = True
            user.status = VerificationStatusEnum.VERIFIED.code
            db.session.commit()
            db.session.refresh(user)
        return user
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Retrieve a user by their ID with rotation city preloaded.
        
        Args:
            user_id: The ID of the user to retrieve
            
        Returns:
            User object with rotation_city relationship loaded, None if not found
        """
        return User.query.options(joinedload(User.rotation_city)).filter_by(user_id=user_id).first()
    
    def get_all_users(self) -> List[User]:
        """Retrieve all users from the database.
        
        Returns:
            List of all User objects
        """
        return User.query.all()
    
    def update(self, user_id: int, **kwargs) -> User:
        """Update user fields in the database.
        
        Only allows updating first_name, last_name, and rotation_city_id.
        
        Args:
            user_id: The ID of the user to update
            **kwargs: Fields to update (first_name, last_name, rotation_city_id)
            
        Returns:
            Updated User object
            
        Raises:
            ValueError: If user is not found
        """
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
