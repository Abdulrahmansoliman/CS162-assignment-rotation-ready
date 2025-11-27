from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()


def create_app(config_name='development'):
    """Application factory function."""
    flask_app = Flask(__name__)
    
    # Load configuration based on environment
    if config_name == 'production':
        from app.config.production import Production
        flask_app.config.from_object(Production)
    elif config_name == 'testing':
        from app.config.testing import Testing
        flask_app.config.from_object(Testing)
    else:
        from app.config.development import Development
        flask_app.config.from_object(Development)
    
    # Initialize extensions
    db.init_app(flask_app)
    jwt.init_app(flask_app)
    
    # Register blueprints
    from app.api.v1 import api_bp
    flask_app.register_blueprint(api_bp)
    
    # Import JWT error handlers to register them
    # This must happen after jwt.init_app()
    import app.api.v1.auth.jwt_handlers  # noqa: F401
    
    # Create database tables
    with flask_app.app_context():
        db.create_all()
    
    return flask_app
