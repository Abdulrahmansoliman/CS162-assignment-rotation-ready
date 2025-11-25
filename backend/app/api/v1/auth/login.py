from flask import Blueprint, request, jsonify
from app.utils.decorators import require_params
from services.auth.login_service import LoginService
from services.auth.token_service import TokenService
from app.api.v1.auth import auth_bp


@auth_bp.route('/login', methods=['POST'])
@require_params('email')
def login():
    """Initiate login by sending verification code."""
    data = request.get_json()
    
    try:
        login_service = LoginService()
        login_service.initiate_login(email=data['email'])

        return jsonify({
            'message': 'Verification code sent to your email.'
        }), 200

    except ValueError as ve:
        return jsonify({'message': str(ve)}), 400

    except Exception as e:
        return jsonify({'message': 'An error occurred during login initiation.'}), 500

@auth_bp.route('/login/verify', methods=['POST'])
@require_params('email', 'verification_code')
def verify_login():
    """Verify login code and authenticate user."""
    data = request.get_json()
    
    try:
        login_service = LoginService()
        user = login_service.verify_login(
            email=data['email'],
            verification_code=data['verification_code']
        )

        tokens = TokenService.generate_tokens(user)

        return jsonify({
            'message': 'Login successful.',
            'user_id': user.user_id,
            'email': user.email,
            'access_token': tokens['access_token'],
            'refresh_token': tokens['refresh_token']
        }), 200

    except ValueError as ve:
        return jsonify({'message': str(ve)}), 400

    except Exception as e:
        return jsonify({'message': 'An error occurred during login verification.'}), 500
