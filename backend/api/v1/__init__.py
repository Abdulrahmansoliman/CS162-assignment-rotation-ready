from backend.api.v1.auth import auth_bp
from backend.api.v1.cities import cities_bp
from backend.api.v1.users import users_bp
from backend.api.v1.categories import categories_bp
from backend.api.v1.rotation_city import places_bp
from backend.api.v1.verifications import verifications_bp


blueprints = [
    auth_bp,
    cities_bp,
    users_bp,
    categories_bp,
    places_bp,
    verifications_bp
]

__all__ = ["blueprints"]