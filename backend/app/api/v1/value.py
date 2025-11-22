from flask import Blueprint, request
from pydantic import BaseModel
from app.api.v1.schemas.schemas import ValueResponse

value_bp = Blueprint('value', __name__, url_prefix='/api/v1/value')


@value_bp.route('/<int:value_id>', methods=['GET'])
def get_value(value_id):
    """Get value by value id"""
    from app.models.value import Value

    value = Value.query.filter_by(value_id=value_id).first()

    if not value:
        return {"error": "Value not found"}, 404
    
    return ValueResponse.from_orm(value).model_dump(), 200