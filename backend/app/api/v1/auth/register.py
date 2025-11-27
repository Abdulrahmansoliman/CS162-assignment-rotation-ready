from app.services.auth.registration_service import RegistrationService
from app.services.auth.token_service import TokenService
from app.services.auth.verification_code_service import RateLimitExceededError
from app.api.v1.auth import auth_bp

from flask import Blueprint, request, jsonify
from app.utils.decorators import require_params


@auth_bp.route('/register', methods=['POST'])
@require_params('email', 'city_id', 'first_name', 'last_name')
def register():
    """User registration endpoint."""
    data = request.get_json()
    
    email = data['email']
    city_id = data['city_id']
    first_name = data['first_name']
    last_name = data['last_name']

    try:
        registration_service = RegistrationService()
        new_user = registration_service.register_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            rotation_city_id=city_id
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
    """User email verification endpoint."""
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
    """Resend verification code endpoint."""
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