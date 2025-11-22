from flask import Blueprint, jsonify
from pydantic import BaseModel
from app.api.v1.schemas.schemas import RotationCityResponse


rotation_city_bp = Blueprint('rotation_city', __name__, url_prefix=("/api/v1/rotation-city"))


@rotation_city_bp.route('/', methods=['GET'])
def get_rotation_cities():
    """Get list of rotation cities"""

    cities = RotationCity.query.all()

    if not cities:
        return jsonify({"error": "Rotation cities not found"})
    
    city_data = [city.name for city in cities]

    return jsonify(city_data), 200