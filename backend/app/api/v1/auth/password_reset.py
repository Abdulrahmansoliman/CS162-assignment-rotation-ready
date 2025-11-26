from flask import request, jsonify
from app.api.v1.auth import auth_bp
from app.utils.decorators import require_params
from app.services.auth.password_reset_service import (
    PasswordResetService,
    InvalidOrExpiredTokenError
)


@auth_bp.route('/password-reset/request', methods=['POST'])
@require_params('email')
def request_password_reset():
    """Request a password reset email."""
    data = request.get_json()
    email = data['email']
    
    try:
        service = PasswordResetService()
        service.request_reset(email)
        
        # Always return success to prevent email enumeration
        return jsonify({
            'message': (
                'If that email exists, '
                'a password reset link has been sent.'
            )
        }), 202
    
    except Exception as e:
        return jsonify({
            'message': 'An error occurred while processing your request.'
        }), 500


@auth_bp.route('/password-reset/verify', methods=['POST'])
@require_params('token', 'new_password')
def verify_password_reset():
    """Verify reset token and update password."""
    data = request.get_json()
    token = data['token']
    new_password = data['new_password']
    
    # Validate password strength
    if len(new_password) < 8:
        return jsonify({
            'message': 'Password must be at least 8 characters long.'
        }), 400
    
    try:
        service = PasswordResetService()
        service.confirm_reset(token, new_password)
        
        return jsonify({
            'message': 'Password updated successfully.'
        }), 200
    
    except InvalidOrExpiredTokenError as e:
        return jsonify({
            'message': str(e)
        }), 400
    
    except Exception as e:
        return jsonify({
            'message': 'An error occurred while resetting your password.'
        }), 500
