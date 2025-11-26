from flask import Blueprint, jsonify

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


# Register rotation_city blueprint
from app.api.v1.rotation_city import rotation_city_bp
api_bp.register_blueprint(rotation_city_bp)
