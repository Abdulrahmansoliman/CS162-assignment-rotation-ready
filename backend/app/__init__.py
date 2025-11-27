from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()


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
