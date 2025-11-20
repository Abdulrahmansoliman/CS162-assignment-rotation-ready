from flask import Blueprint, request, jsonify
from pydantic import BaseModel, EmailStr, ValidationError


auth_bp = Blueprint('auth', __name__, url_prefix='api/v1/auth')


class MagicLinkRequest(BaseModel):
    """Request schema for magic link"""
    email: EmailStr


class MagicLinkResponse(BaseModel):
    """Response after requesting the magic link"""
    email: EmailStr
    message: str


class TokenResponse(BaseModel):
    """Response from the magic link"""
    access_token: str
    token_type: str


@auth_bp.route('/magic-link', methods=['POST'])
def request_magic_link():
    """send magic link to users email if it ends with a minerva.edu email"""
    try:
        # validate request data
        data = MagicLinkRequest(**request.get_json())

        # validate minerva email domain
        if not data.email.endswith('minerva.edu'):
            return jsonify({'error': 'Only minerva emails are allowed'})
        
        # TODO: generate the magic link

        return jsonify({
            'message': 'Magic link sent to your address',
            'email': data.email
        }), 200
    
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    

@auth_bp.route('/verify/<token>', methods=['GET'])
def verify_magic_token(token):
    """verify magic link token"""

    # TODO: verify token from db

    return jsonify({
        'access_token': 'token',
        'token_type': 'bearer'
    })