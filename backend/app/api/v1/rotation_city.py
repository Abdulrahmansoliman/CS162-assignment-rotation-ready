from flask import jsonify, Blueprint
from app.services.rotation_city_service import RotationCityService
from app.api.v1.schemas.rotation_city_schema import RotationCityResponse

rotation_city_bp = Blueprint('rotation_city', __name__)


@rotation_city_bp.route('/', methods=['GET'])
def get_rotation_cities():
    """Get list of all rotation cities"""
    service = RotationCityService()

    cities = service.get_all_rotation_cities()

    # Return empty array if no cities (standard REST practice)
    if not cities:
        return jsonify([]), 200

    return jsonify([RotationCityResponse.model_validate(city).model_dump() for city in cities]), 200


@rotation_city_bp.route('/<int:city_id>', methods=['GET'])
def get_rotation_city(city_id):
    """Get rotation city by city_id"""
    service = RotationCityService()

    city = service.get_rotation_city(city_id)

    if not city:
        return jsonify({"error": "Rotation city not found"}), 404

    return jsonify(RotationCityResponse.model_validate(city).model_dump()), 200
