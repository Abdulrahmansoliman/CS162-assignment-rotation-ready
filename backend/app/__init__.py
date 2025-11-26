from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()


@jwt.expired_token_loader
def handle_expired_token(jwt_header, jwt_payload):
    """Return a consistent response when tokens expire."""
    return jsonify({'message': 'Token has expired.'}), 401


@jwt.invalid_token_loader
def handle_invalid_token(error):
    """Return response for malformed or otherwise invalid tokens."""
    return jsonify({'message': 'Invalid token.', 'error': error}), 401


@jwt.unauthorized_loader
def handle_missing_token(error):
    """Return response when Authorization header is missing."""
    return jsonify({
        'message': 'Missing authorization token.',
        'error': error
    }), 401


@jwt.needs_fresh_token_loader
def handle_fresh_token_required(jwt_header, jwt_payload):
    """Return response when a fresh token is required for the endpoint."""
    return jsonify({'message': 'Fresh token required.'}), 401


@jwt.revoked_token_loader
def handle_revoked_token(jwt_header, jwt_payload):
    """Return response when a revoked token is encountered."""
    return jsonify({'message': 'Token has been revoked.'}), 401


def create_app(config_name='development'):
    """Application factory function."""
    app = Flask(__name__)
    
    # Load configuration based on environment
    if config_name == 'production':
        from app.config.production import Production
        app.config.from_object(Production)
    elif config_name == 'testing':
        from app.config.testing import Testing
        app.config.from_object(Testing)
    else:
        from app.config.development import Development
        app.config.from_object(Development)
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    
    # Register blueprints
    from app.api.v1 import api_bp
    app.register_blueprint(api_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
