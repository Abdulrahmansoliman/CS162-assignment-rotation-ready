from flask import Blueprint, request, jsonify
from app.utils.decorators import require_params
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.user_service import UserService
from app.api.v1.schemas.user_schema import UserResponse

user_bp = Blueprint('user', __name__)

_user_service: UserService = UserService()


def _serialize_user(user):
    """Serialize user model to response dictionary.
    
    Args:
        user: User model instance
        
    Returns:
        Dictionary with user data validated by UserResponse schema
    """
    return UserResponse.model_validate(user).model_dump()

@user_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current authenticated user's information.
    
    Returns details for the user identified by the JWT token.
    
    Headers:
        Authorization: Bearer <access_token>
        
    Returns:
        200: User information including rotation city
        404: User not found
        500: Internal server error
    """
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
    """Get verified user by user ID.
    
    Returns information for a specific verified user.
    
    Path Parameters:
        user_id (int): The ID of the user to retrieve
        
    Headers:
        Authorization: Bearer <access_token>
        
    Returns:
        200: User information
        404: User not found or not verified
        500: Internal server error
    """
    user = _user_service.get_verified_user_by_id(user_id)

    if user is None:
        return jsonify({'message': 'User not found.'}), 404

    return jsonify(_serialize_user(user)), 200

@user_bp.route('/me', methods=['PUT'])
@jwt_required()
def update_current_user():
    """Update current authenticated user's information.
    
    Allows updating first_name, last_name, and rotation_city_id.
    
    Headers:
        Authorization: Bearer <access_token>
        
    Request Body:
        first_name (str, optional): New first name
        last_name (str, optional): New last name
        rotation_city_id (int, optional): New rotation city ID
        
    Returns:
        200: User updated successfully
        404: User not found
        500: Internal server error
    """
    user_id = get_jwt_identity()
    data = request.json

    try:
        user = _user_service.update_user(user_id, data)

        if user is None:
            return jsonify({'message': 'User not found.'}), 404

        return jsonify(_serialize_user(user)), 200

    except Exception as e:
        return jsonify({'message': 'An error occurred while updating user data.'}), 500