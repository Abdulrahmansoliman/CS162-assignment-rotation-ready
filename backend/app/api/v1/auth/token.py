"""Authentication token refresh endpoints."""
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.api.v1.auth import auth_bp
from app.repositories.implementations.user_repository import UserRepository
from app.services.auth.token_service import TokenService


_user_repository = UserRepository()


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_access_token():
    """Generate a new access token for the authenticated user."""
    user_id = get_jwt_identity()
    user = None
    if user_id is not None:
        user = _user_repository.get_user_by_id(int(user_id))

    if not user:
        return jsonify({'message': 'User not found.'}), 404

    new_access_token = TokenService.generate_access_token(user)
    return jsonify({'access_token': new_access_token}), 200
