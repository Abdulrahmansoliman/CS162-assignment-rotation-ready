from flask import Blueprint, request, jsonify
from pydantic import BaseModel, EmailStr, ValidationError
from functools import wraps
import random
import string
from datetime import datetime, timedelta


auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


# Helper decorator for required parameters
def require_params(*required_params):
    """Decorator to validate required parameters in request"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Request body is required'}), 400
            
            missing_params = [param for param in required_params if param not in data]
            if missing_params:
                return jsonify({
                    'error': f'Missing required parameters: {", ".join(missing_params)}'
                }), 400
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def generate_otp(length=6):
    """Generate a 6-character OTP (digits and uppercase letters)"""
    characters = string.digits + string.ascii_uppercase
    return ''.join(random.choice(characters) for _ in range(length))


# Request/Response Schemas
class RegisterRequest(BaseModel):
    """Request schema for registration"""
    email: EmailStr
    city_id: int
    first_name: str
    last_name: str


class VerifyRequest(BaseModel):
    """Request schema for OTP verification"""
    email: EmailStr
    verification_code: str


class LoginRequest(BaseModel):
    """Request schema for login"""
    email: EmailStr


class AuthResponse(BaseModel):
    """Response after successful verification"""
    user_id: int
    access_token: str
    token_type: str = "bearer"


# Endpoints
@auth_bp.route('/register', methods=['POST'])
@require_params('email', 'city_id', 'first_name', 'last_name')
def register():
    """
    Register new user and send OTP to email
    Returns 201 if successful - frontend should show OTP form
    """
    try:
        data = RegisterRequest(**request.get_json())
        
        # Validate Minerva email domain
        if not data.email.endswith('@uni.minerva.edu'):
            return jsonify({'error': 'Only Minerva emails are allowed'}), 400
        
        # TODO: Check if user already exists
        # TODO: Validate city_id exists
        
        # Generate OTP
        otp = generate_otp()
        expiry = datetime.utcnow() + timedelta(minutes=15)  # Default 15 min expiry
        
        # TODO: Store OTP in database/cache with expiry time
        # TODO: Store pending registration data (email, city_id, first_name, last_name)
        # TODO: Send OTP email
        
        print(f"DEBUG: OTP for {data.email}: {otp}")  # Remove in production
        
        return jsonify({
            'message': 'Verification code sent to your email',
            'email': data.email
        }), 201
        
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400


@auth_bp.route('/register/verify', methods=['POST'])
@require_params('email', 'verification_code')
def register_verify():
    """
    Verify OTP for registration
    Returns 200 with user_id and JWT if successful
    """
    try:
        data = VerifyRequest(**request.get_json())
        
        # TODO: Retrieve OTP from database/cache
        # TODO: Check if OTP is valid and not expired
        # TODO: Retrieve pending registration data
        # TODO: Create user in database
        # TODO: Delete OTP from cache
        # TODO: Generate JWT token
        
        # Stub response
        return jsonify({
            'user_id': 1,
            'access_token': 'stub_jwt_token',
            'token_type': 'bearer'
        }), 200
        
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400


@auth_bp.route('/login', methods=['POST'])
@require_params('email')
def login():
    """
    Login existing user and send OTP to email
    Returns 200 if successful - frontend should show OTP form
    """
    try:
        data = LoginRequest(**request.get_json())
        
        # Validate Minerva email domain
        if not data.email.endswith('@uni.minerva.edu'):
            return jsonify({'error': 'Only Minerva emails are allowed'}), 400
        
        # TODO: Check if user exists
        # If user doesn't exist, return 404
        
        # Generate OTP
        otp = generate_otp()
        expiry = datetime.utcnow() + timedelta(minutes=15)  # Default 15 min expiry
        
        # TODO: Store OTP in database/cache with expiry time
        # TODO: Send OTP email
        
        print(f"DEBUG: OTP for {data.email}: {otp}")  # Remove in production
        
        return jsonify({
            'message': 'Verification code sent to your email',
            'email': data.email
        }), 200
        
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400


@auth_bp.route('/login/verify', methods=['POST'])
@require_params('email', 'verification_code')
def login_verify():
    """
    Verify OTP for login
    Returns 200 with user_id and JWT if successful
    """
    try:
        data = VerifyRequest(**request.get_json())
        
        # TODO: Retrieve OTP from database/cache
        # TODO: Check if OTP is valid and not expired
        # TODO: Get user from database
        # TODO: Delete OTP from cache
        # TODO: Generate JWT token
        
        # Stub response
        return jsonify({
            'user_id': 1,
            'access_token': 'stub_jwt_token',
            'token_type': 'bearer'
        }), 200
        
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
