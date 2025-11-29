from flask import jsonify, Blueprint
from app.services.value_service import ValueService
from app.api.v1.schemas.value_schema import ValueSchemaResponse

value_bp = Blueprint('value', __name__)


@value_bp.route('/', methods=['GET'])
def get_values():

    service = ValueService()

    values = service.get_all_values()

    if not values:
        return jsonify({'error':'No values found'}), 404
    
    return jsonify([ValueSchemaResponse.model_validate(values).model_dump() for value in values]), 200
