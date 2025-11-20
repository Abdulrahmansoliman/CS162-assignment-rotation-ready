from backend.api.v1.auth import auth_bp
from backend.api.v1.rotation_city import rotation_city_bp
from backend.api.v1.user import user_bp
from backend.api.v1.categories import categories_bp
from backend.api.v1.item import item_bp
from backend.api.v1.value import value_bp
from backend.api.v1.verification import verification_bp


blueprints = [
    auth_bp,
    rotation_city_bp,
    user_bp,
    categories_bp,
    item_bp,
    value_bp,
    verification_bp
]

__all__ = ["blueprints"]