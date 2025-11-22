from flask import Blueprint
from app.api.v1.auth import auth_bp
from app.api.v1.rotation_city import rotation_city_bp
from app.api.v1.user import user_bp
from app.api.v1.categories import categories_bp
from app.api.v1.item import item_bp
from app.api.v1.value import value_bp
from app.api.v1.verification import verification_bp

# Create a parent blueprint
api_bp = Blueprint('api', __name__)

# Register all sub-blueprints
blueprints = [
    auth_bp,
    rotation_city_bp,
    user_bp,
    categories_bp,
    item_bp,
    value_bp,
    verification_bp
]

__all__ = ["api_bp", "blueprints"]
