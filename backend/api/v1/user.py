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
    users = []  # TODO: query the database for the user by id

    return jsonify({'user': [UserResponse(
        user_id=user.user_id,
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        created_at=user.created_at,
        updated_at=user.updated_at
    ).model_dump() for user in users]})