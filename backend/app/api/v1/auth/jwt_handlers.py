"""JWT error handlers for authentication."""
from flask import jsonify
from app import jwt


@jwt.expired_token_loader
def handle_expired_token(jwt_header, jwt_payload):
    """
    Handle expired JWT tokens.
    
    Returns:
        JSON response with 401 status code
    """
    return jsonify({'message': 'Token has expired.'}), 401


@jwt.invalid_token_loader
def handle_invalid_token(error):
    """
    Handle malformed or otherwise invalid tokens.
    
    Args:
        error: Error message describing why the token is invalid
        
    Returns:
        JSON response with 401 status code
    """
    return jsonify({'message': 'Invalid token.', 'error': error}), 401


@jwt.unauthorized_loader
def handle_missing_token(error):
    """
    Handle missing Authorization header.
    
    Args:
        error: Error message describing the missing token
        
    Returns:
        JSON response with 401 status code
    """
    return jsonify({
        'message': 'Missing authorization token.',
        'error': error
    }), 401


@jwt.needs_fresh_token_loader
def handle_fresh_token_required(jwt_header, jwt_payload):
    """
    Handle requests that require a fresh token.
    
    Returns:
        JSON response with 401 status code
    """
    return jsonify({'message': 'Fresh token required.'}), 401
