from flask import jsonify
from pydantic import BaseModel
from app.api.v1.rotation_city import rotation_city_bp
from app.services.rotation_city_service import RotationCityService

# Create service instance
rotation_city_service = RotationCityService()


class RotationCityResponse(BaseModel):
    """Response schema for rotation city"""
    city_id: int
    name: str
    time_zone: str
    res_hall_location: str | None = None

    class Config:
        from_attributes = True


@rotation_city_bp.route('/', methods=['GET'])
def get_rotation_cities():
    """Get list of all rotation cities"""
    cities = rotation_city_service.get_all_rotation_cities()

    if not cities:
        return jsonify({"error": "No rotation cities found"}), 404

    city_data = [
        RotationCityResponse.model_validate(city).model_dump()
        for city in cities
    ]

    return jsonify(city_data), 200


@rotation_city_bp.route('/<int:city_id>', methods=['GET'])
def get_rotation_city(city_id):
    """Get rotation city by city_id"""
    city = rotation_city_service.get_rotation_city(city_id=city_id)

    if not city:
        return jsonify({"error": "Rotation city not found"}), 404

    return jsonify(
        RotationCityResponse.model_validate(city).model_dump()
    ), 200
