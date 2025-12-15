from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS
import os

db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()


def create_app(config_name='development'):
    """Application factory function."""
    from app.config.production import Production
    from app.config.testing import Testing
    from app.config.development import Development
    
    app = Flask(__name__)
    # Allow routes to be accessed with or without a trailing slash to avoid
    # 308 redirects on OPTIONS preflight requests (prevents CORS/redirect issues)
    app.url_map.strict_slashes = False
    
    # Load configuration based on environment
    if config_name == 'production':
        app.config.from_object(Production)
    elif config_name == 'testing':
        app.config.from_object(Testing)
    else:
        app.config.from_object(Development)
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    
    # Enable CORS with configurable origins
    cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')
    
    CORS(app, resources={
        r"/api/*": {
            "origins": cors_origins,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    
    # Register blueprints and JWT handlers
    from app.api.v1 import api_bp
    from app.api.v1.auth import jwt_handlers
    
    app.register_blueprint(api_bp)

    # Root health check to avoid noisy 404s on HEAD/GET /
    @app.route('/', methods=['GET'])
    def root():
        return {'status': 'ok'}, 200
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
