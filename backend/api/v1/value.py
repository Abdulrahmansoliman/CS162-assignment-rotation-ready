from flask import Blueprint, request
from pydantic import BaseModel


value_bp = Blueprint('value', __name__, url_prefix='/api/v1/value')


class ValueResponse(BaseModel):
    """Response schema for value"""
    value_id: int
    tag_id: int
    boolean_val: bool
    name_val: str
    number_val: float

@value_bp.route('/<int:value_id>', methods=['GET'])
