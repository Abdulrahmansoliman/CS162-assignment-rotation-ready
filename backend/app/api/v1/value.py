from flask import Blueprint, request, jsonify
from pydantic import BaseModel
from app.api.v1.schemas.schemas import ValueResponse
from app.services.value_service import ValueService

value_bp = Blueprint('value', __name__, url_prefix='/api/v1/value')


@value_bp.route('/<int:value_id>', methods=['GET'])
def get_value(value_id):
    """Get value by value id"""
    value = ValueService.get_value(value_id=value_id)

    if not value:
        return jsonify({"error": "Value not found"}), 404

    return jsonify(ValueResponse.model_validate(value).model_dump()), 200