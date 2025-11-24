from flask import Blueprint, request, jsonify
from utils.decorators import require_params

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
@require_params('email')
def login():
    """Initiate login by sending verification code."""
    data = request.get_json()
    
    try:
        from services.auth.login_service import LoginService
        
        login_service = LoginService()
        login_service.initiate_login(email=data['email'])

        return jsonify({
            'message': 'Verification code sent to your email.'
        }), 200

    except ValueError as ve:
        return jsonify({'message': str(ve)}), 400

    except Exception as e:
        return jsonify({'message': 'An error occurred during login initiation.'}), 500
