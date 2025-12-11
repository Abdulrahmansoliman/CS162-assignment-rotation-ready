from flask import jsonify, Blueprint, request
from app.services.value_service import ValueService
from app.api.v1.schemas.value_schema import ValueSchemaResponse
from flask_jwt_extended import jwt_required

value_bp = Blueprint('value', __name__)
service = ValueService()

@value_bp.route('/', methods=['GET'])
@jwt_required()
def get_values():
    """Get all values"""
    values = service.get_all_values()

    if not values:
        return jsonify({'error': 'No values found'}), 404
    
    return jsonify([ValueSchemaResponse.model_validate(value).model_dump() for value in values]), 200





@value_bp.route('/tag/<int:tag_id>', methods=['GET'])
@jwt_required()
def get_text_values_by_tag(tag_id):
    """Get all text values for a specific tag.
    """
    values = service.get_text_values_by_tag(tag_id)

    if not values:
        return jsonify({'error': 'No text values found for this tag'}), 404
    
    return jsonify([
        ValueSchemaResponse.model_validate(value).model_dump()
        for value in values
    ]), 200


@value_bp.route('/<int:value_id>', methods=['GET'])
@jwt_required()
def get_value_by_id(value_id):
    """Get value by ID"""
    value = service.get_value_by_id(value_id)

    if not value:
        return jsonify({'error': 'Value not found'}), 404
    
    return jsonify(ValueSchemaResponse.model_validate(value).model_dump()), 200


@value_bp.route('/', methods=['POST'])
@jwt_required()
def add_value():
    """Create new value"""
    data = request.get_json()

    if not data or 'tag_id' not in data:
        return jsonify({'error': 'tag_id is required'}), 400
    
    value = service.add_value(
        tag_id=data['tag_id'],
        boolean_val=data.get('boolean_val'),
        name_val=data.get('name_val'),
        numerical_value=data.get('numerical_value')
    )

    if not value:
        return jsonify({'error': 'Failed to create value'}), 500
    
    return jsonify(ValueSchemaResponse.model_validate(value).model_dump()), 201


@value_bp.route('/<int:value_id>', methods=['PUT'])
@jwt_required()
def update_value(value_id):
    """Update value"""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    value = service.update_value(
        value_id=value_id,
        tag_id=data.get('tag_id'),
        boolean_val=data.get('boolean_val'),
        name_val=data.get('name_val'),
        numerical_value=data.get('numerical_value')
    )

    if not value:
        return jsonify({'error': 'Value not found'}), 404
    
    return jsonify(ValueSchemaResponse.model_validate(value).model_dump()), 200


@value_bp.route('/<int:value_id>', methods=['DELETE'])
@jwt_required()
def delete_value(value_id):
    """Delete value"""
    success = service.delete_value(value_id)

    if not success:
        return jsonify({'error': 'Value not found'}), 404
    
    return jsonify({'message': 'Value deleted successfully'}), 200
