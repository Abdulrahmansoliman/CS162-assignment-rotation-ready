from flask import Flask
from flask_cors import CORS
from backend.api.v1 import blueprints


def create_app():
    app = Flask(__name__)
    
    # CORS
    CORS(app)
    
    # Configuration
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    
    # Register all blueprints
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
    
    @app.route('/')
    def index():
        return {"message": "Rotation Finder API", "version": "1.0.0"}
    
    @app.route('/health')
    def health():
        return {"status": "healthy"}
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)