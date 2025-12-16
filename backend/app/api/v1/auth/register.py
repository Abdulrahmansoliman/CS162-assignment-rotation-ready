from app.services.auth.registration_service import RegistrationService
from app.services.auth.token_service import TokenService
from app.services.auth.verification_code_service import RateLimitExceededError
from app.api.v1.auth import auth_bp

from flask import Blueprint, request, jsonify
from app.utils.decorators import require_params


@auth_bp.route('/register', methods=['POST'])
@require_params('email', 'city_id', 'first_name', 'last_name')
def register():
    """Register a new user account.
    
    Creates a new user and sends a verification code email.
    If user exists but is unverified, resends verification code.
    
    Request Body:
        email (str): User's email address
        city_id (int): ID of user's current rotation city
        first_name (str): User's first name
        last_name (str): User's last name
        profile_picture (str, optional): Base64 encoded profile picture
        
    Returns:
        201: User registered successfully, verification email sent
        200: Verification code resent for existing unverified user
        400: User already verified or validation error
        429: Rate limit exceeded for verification codes
        500: Internal server error
    """
    data = request.get_json()
    
    email = data['email']
    city_id = data['city_id']
    first_name = data['first_name']
    last_name = data['last_name']

    profile_picture = data.get('profile_picture', None)

    try:
        registration_service = RegistrationService()
        new_user = registration_service.register_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            rotation_city_id=city_id,
            profile_picture=profile_picture
        )
        if new_user is None:
            return jsonify({'message': 'Verification code resent. Please check your email.'}), 200

        return jsonify({
            'message': 'User registered successfully. Please verify your email.',
            'user_id': new_user.user_id
        }), 201

    except RateLimitExceededError as rle:
        return jsonify({'message': str(rle)}), 429

    # verified user exists
    except ValueError as ve:
        return jsonify({'message': str(ve)}), 400

    except Exception as e:
        return jsonify({'message': 'An error occurred during registration.'}), 500
    
@auth_bp.route('/register/verify', methods=['POST'])
@require_params('email', 'verification_code')
def verify_registration():
    """Verify user email with verification code.
    
    Validates the verification code and marks user as verified.
    Returns access and refresh tokens upon successful verification.
    
    Request Body:
        email (str): User's email address
        verification_code (str): 6-digit verification code from email
        
    Returns:
        200: Email verified successfully with JWT tokens
        400: Invalid or expired verification code
        500: Internal server error
    """
    data = request.get_json()
    
    try:        
        registration_service = RegistrationService()
        user = registration_service.verify_user_email(
            email=data['email'],
            verification_code=data['verification_code']
        )

        tokens = TokenService.generate_tokens(user)

        return jsonify({
            'message': 'Email verified successfully.',
            'user_id': user.user_id,
            'email': user.email,
            'access_token': tokens['access_token'],
            'refresh_token': tokens['refresh_token']
        }), 200

    except ValueError as ve:
        return jsonify({'message': str(ve)}), 400

    except Exception as e:
        return jsonify({'message': 'An error occurred during email verification.'}), 500

@auth_bp.route('/register/resend-code', methods=['POST'])
@require_params('email')
def resend_verification_code():
    """Resend verification code to user's email.
    
    Generates and sends a new verification code for unverified users.
    
    Request Body:
        email (str): User's email address
        
    Returns:
        200: Verification code resent successfully
        400: User not found or already verified
        429: Rate limit exceeded
        500: Internal server error
    """
    data = request.get_json()
    
    try:        
        registration_service = RegistrationService()
        registration_service.resend_verification_code(email=data['email'])

        return jsonify({
            'message': 'Verification code resent. Please check your email.'
        }), 200

    except RateLimitExceededError as rle:
        return jsonify({'message': str(rle)}), 429

    except ValueError as ve:
        return jsonify({'message': str(ve)}), 400

    except Exception as e:
        return jsonify({'message': 'An error occurred while resending verification code.'}), 500