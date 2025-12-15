import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from app import create_app

# Get environment from OS variable, default to 'development'
config_name = os.getenv('FLASK_ENV', 'development')

# Create the Flask app
app = create_app(config_name)

if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )