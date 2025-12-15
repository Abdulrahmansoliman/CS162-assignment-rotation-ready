from flask import Blueprint, request, jsonify
from app.utils.decorators import require_params
from app.services.auth.login_service import LoginService
from app.services.auth.token_service import TokenService
from app.services.auth.verification_code_service import RateLimitExceededError
from app.api.v1.auth import auth_bp


@auth_bp.route('/login', methods=['POST'])
@require_params('email')
def login():
    """Initiate login process by sending verification code.
    
    Sends a verification code to the user's email for passwordless login.
    User must be already registered and verified.
    
    Request Body:
        email (str): User's email address
        
    Returns:
        200: Verification code sent to email
        400: User not found or not verified
        429: Rate limit exceeded for verification codes
        500: Internal server error
    """
    data = request.get_json()
    
    try:
        login_service = LoginService()
        login_service.initiate_login(email=data['email'])

        return jsonify({
            'message': 'Verification code sent to your email.'
        }), 200

    except ValueError as ve:
        return jsonify({'message': str(ve)}), 400
    
    except RateLimitExceededError as rle:
        return jsonify({'message': str(rle)}), 429  

    except Exception as e:
        return jsonify({'message': 'An error occurred during login initiation.'}), 500

@auth_bp.route('/login/verify', methods=['POST'])
@require_params('email', 'verification_code')
def verify_login():
    """Verify login code and authenticate user.
    
    Validates the verification code sent to user's email and returns JWT tokens.
    
    Request Body:
        email (str): User's email address
        verification_code (str): 6-digit verification code from email
        
    Returns:
        200: Login successful with access and refresh tokens
        400: Invalid or expired verification code
        500: Internal server error
    """
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
