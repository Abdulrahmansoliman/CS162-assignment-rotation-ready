from flask import jsonify, Blueprint
from app.services.rotation_city_service import RotationCityService
from app.api.v1.schemas.rotation_city_schema import RotationCityResponse

rotation_city_bp = Blueprint('rotation_city', __name__)


@rotation_city_bp.route('/', methods=['GET'])
def get_rotation_cities():
    """Get list of all Minerva rotation cities.
    
    Public endpoint - no authentication required.
    
    Returns:
        200: List of all rotation cities (empty array if none exist)
    """
    service = RotationCityService()

    cities = service.get_all_rotation_cities()

    # Return empty array if no cities
    if not cities:
        return jsonify([]), 200

    return jsonify([RotationCityResponse.model_validate(city).model_dump() for city in cities]), 200


@rotation_city_bp.route('/<int:city_id>', methods=['GET'])
def get_rotation_city(city_id):
    """Get a specific rotation city by ID.
    
    Public endpoint - no authentication required.
    
    Path Parameters:
        city_id (int): The ID of the rotation city to retrieve
        
    Returns:
        200: Rotation city information
        404: Rotation city not found
    """
    service = RotationCityService()

    city = service.get_rotation_city(city_id)

    if not city:
        return jsonify({"error": "Rotation city not found"}), 404

    return jsonify(RotationCityResponse.model_validate(city).model_dump()), 200
