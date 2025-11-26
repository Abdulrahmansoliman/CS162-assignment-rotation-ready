from flask import Blueprint

rotation_city_bp = Blueprint(
    'rotation_city',
    __name__,
    url_prefix="/api/v1/rotation-city"
)

from app.api.v1.rotation_city import routes
