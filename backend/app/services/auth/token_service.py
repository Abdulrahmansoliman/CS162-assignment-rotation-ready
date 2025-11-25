"""JWT token service for authentication."""
from flask_jwt_extended import create_access_token, create_refresh_token
from app.models.user import User
from flask import current_app


class TokenService:
    """Service for generating and managing JWT tokens."""

    @staticmethod
    def generate_tokens(user: User) -> dict:
        """Generate access and refresh tokens for user.
        
        Args:
            user: User model instance
            
        Returns:
            Dictionary with access_token and refresh_token
        """
        access_token = create_access_token(
            identity=str(user.user_id),
            additional_claims={
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        )
        
        refresh_token = create_refresh_token(identity=str(user.user_id))
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    @staticmethod
    def generate_access_token(user: User) -> str:
        """Generate a new access token from refresh token.
        
        Args:
            user: User model instance
            
        Returns:
            New access token string
        """
        return create_access_token(
            identity=str(user.user_id),
            additional_claims={
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        )
