from flask import Blueprint, jsonify
from pydantic import BaseModel


rotation_city_bp = Blueprint('rotation_city', __name__, url_prefix=("/api/v1/rotation-city"))


class RotationCityResponse(BaseModel):
    """Response schema for rotation city"""
    city_id: int
    city_name: str
    timezone: str


@rotation_city_bp.route('/', methods=['GET'])
def get_rotation_cities():
    """Get list of rotation cities"""

    # TODO: query the database for rotation cities

    cities = [] 
    return jsonify({"cities": 
                    [RotationCityResponse(
                        city_id=city.city_id,
                        city_name=city.city_name, 
                        timezone=city.timezone
                        ).model_dump() 
                        for city in cities]}), 200