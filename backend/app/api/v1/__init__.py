from flask import Blueprint, jsonify
from .rotation_city import rotation_city_bp
from .auth import auth_bp
from .value import value_bp
from .user import user_bp

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'message': 'API is running'}), 200


@api_bp.route('/', methods=['GET'])
def index():
    """API welcome endpoint."""
    return jsonify({
        'message': 'Welcome to Minerva API v1',
        'version': '1.0.0'
    }), 200


api_bp.register_blueprint(rotation_city_bp, url_prefix='/rotation-city')

api_bp.register_blueprint(auth_bp, url_prefix='/auth')

api_bp.register_blueprint(user_bp, url_prefix='/user')

api_bp.register_blueprint(value_bp, url_prefix='/value')