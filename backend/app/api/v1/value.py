from flask import jsonify, Blueprint, request
from app.services.value_service import ValueService
from app.api.v1.schemas.value_schema import ValueSchemaResponse
from flask_jwt_extended import jwt_required

value_bp = Blueprint('value', __name__)
service = ValueService()

@value_bp.route('/', methods=['GET'])
@jwt_required()
def get_values():
    """Get all values in the system.
    
    Headers:
        Authorization: Bearer <access_token>
    
    Returns:
        200: List of all values
        404: No values found
    """
    values = service.get_all_values()

    if not values:
        return jsonify({'error': 'No values found'}), 404
    
    return jsonify([ValueSchemaResponse.model_validate(value).model_dump() for value in values]), 200





@value_bp.route('/tag/<int:tag_id>', methods=['GET'])
@jwt_required()
def get_text_values_by_tag(tag_id):
    """Get all text values for a specific tag.
    
    Returns only text-type values for the specified tag.
    Useful for populating dropdowns or autocomplete fields.
    
    Path Parameters:
        tag_id (int): The ID of the tag to get values for
        
    Headers:
        Authorization: Bearer <access_token>
    
    Returns:
        200: List of text values for the tag
        404: No text values found for this tag
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
    """Get a specific value by ID.
    
    Path Parameters:
        value_id (int): The ID of the value to retrieve
        
    Headers:
        Authorization: Bearer <access_token>
    
    Returns:
        200: Value information
        404: Value not found
    """
    value = service.get_value_by_id(value_id)

    if not value:
        return jsonify({'error': 'Value not found'}), 404
    
    return jsonify(ValueSchemaResponse.model_validate(value).model_dump()), 200


@value_bp.route('/', methods=['POST'])
@jwt_required()
def add_value():
    """Create a new value for a tag.
    
    Headers:
        Authorization: Bearer <access_token>
        
    Request Body:
        tag_id (int): The ID of the tag this value belongs to (required)
        boolean_val (bool, optional): Boolean value for boolean tags
        name_val (str, optional): Text value for text tags
        numerical_value (float, optional): Numeric value for numeric tags
    
    Returns:
        201: Value created successfully
        400: Missing required field (tag_id)
        500: Failed to create value
    """
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
    """Update an existing value.
    
    Path Parameters:
        value_id (int): The ID of the value to update
        
    Headers:
        Authorization: Bearer <access_token>
        
    Request Body:
        boolean_val (bool, optional): New boolean value
        name_val (str, optional): New text value
        numerical_value (float, optional): New numeric value
    
    Returns:
        200: Value updated successfully
        400: No data provided
        404: Value not found
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    value = service.update_value(
        value_id=value_id,
        boolean_val=data.get('boolean_val'),
        name_val=data.get('name_val'),
        numerical_value=data.get('numerical_value')
    )

    if not value:
        return jsonify({'error': 'Value not found'}), 404
    
    return jsonify(ValueSchemaResponse.model_validate(value).model_dump()), 200

