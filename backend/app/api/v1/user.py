from flask import Blueprint, jsonify
from pydantic import BaseModel


user_bp = Blueprint('user', __name__, url_prefix='/api/v1/user')


class UserResponse(BaseModel):
    """Response schema for user"""
    user_id: int
    username: str
    email: str
    first_name: str
    last_name: str
    created_at: str
    updated_at: str


@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by user id"""
    from app.models.user import User

    user = User.query.filter_by(user_id=user_id)

    if not user:
        return jsonify({"error": "User not found"})
    
    return jsonify(UserResponse.from_orm(user).model_dump()), 200