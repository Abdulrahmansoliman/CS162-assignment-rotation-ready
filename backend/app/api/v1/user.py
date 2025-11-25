from flask import Blueprint, jsonify
from pydantic import BaseModel
from app.services.user_service import UserService


user_bp = Blueprint('user', __name__, url_prefix='/api/v1/user')

# Create service instance
user_service = UserService()


class UserResponse(BaseModel):
    """Response schema for user"""
    user_id: int
    email: str
    first_name: str
    last_name: str

    class Config:
        from_attributes = True


@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by user id"""
    user = user_service.get_user(user_id=user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(UserResponse.model_validate(user).model_dump()), 200
