from flask import Blueprint, request, jsonify
from app.utils.decorators import require_params
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.user_service import UserService
from app.api.v1.schemas.user_schema import UserResponse

user_bp = Blueprint('user', __name__)

_user_service: UserService = UserService()


def _serialize_user(user):
    """Serialize user model to response dictionary."""
    return UserResponse.model_validate(user).model_dump()

@user_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current authenticated user's information."""
    user_id = get_jwt_identity()
    
    try:
        user = _user_service.get_user_by_id(user_id)

        if user is None:
            return jsonify({'message': 'User not found.'}), 404

        return jsonify(_serialize_user(user)), 200

    except Exception as e:
        return jsonify({'message': 'An error occurred while fetching user data.'}), 500
    
@user_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """Get user by user_id"""
    user = _user_service.get_verified_user_by_id(user_id)

    if user is None:
        return jsonify({'message': 'User not found.'}), 404

    return jsonify(_serialize_user(user)), 200

@user_bp.route('/me', methods=['PUT'])
@jwt_required()
def update_current_user():
    """Update current authenticated user's information."""
    user_id = get_jwt_identity()
    data = request.json

    try:
        user = _user_service.update_user(user_id, data)

        if user is None:
            return jsonify({'message': 'User not found.'}), 404

        return jsonify(_serialize_user(user)), 200

    except Exception as e:
        return jsonify({'message': 'An error occurred while updating user data.'}), 500