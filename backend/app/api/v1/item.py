"""Item endpoints."""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from pydantic import ValidationError

from app.services.item_service import ItemService
from app.api.v1.schemas.item_schema import CreateItemRequest, ItemResponse

item_bp = Blueprint('item', __name__)

_item_service = ItemService()


@item_bp.route('/', methods=['POST'])
@jwt_required()
def create_item():
    """
    Create a new item with categories and tags.
    
    Request Body:
        name: Item name
        location: Item location
        walking_distance: Optional walking distance in meters
        category_ids: List of category IDs (at least one required)
        existing_tags: List of {tag_id, value} for existing tags
        new_tags: List of {name, value_type, value} for new tags
    
    Returns:
        201: Item created successfully
        400: Validation error
        500: Internal server error
    """
    user_id = get_jwt_identity()
    
    # Validate request body exists
    if not request.json:
        return jsonify({'message': 'Request body is required'}), 400
    
    try:
        # Validate input with Pydantic
        validated_data = CreateItemRequest(**request.json)
        
        # Get user's rotation_city_id (assuming it's stored in user profile)
        # For now, we'll need to pass it or get it from the user service
        # TODO: Get rotation_city_id from authenticated user
        from app.services.user_service import UserService
        user_service = UserService()
        user = user_service.get_user_by_id(user_id)
        
        if not user or not user.rotation_city_id:
            return jsonify({'message': 'User rotation city not found'}), 400
        
        # Create item
        item = _item_service.create_item(
            name=validated_data.name,
            location=validated_data.location,
            rotation_city_id=user.rotation_city_id,
            added_by_user_id=user_id,
            category_ids=validated_data.category_ids,
            existing_tags=[tag.model_dump() for tag in validated_data.existing_tags],
            new_tags=[tag.model_dump() for tag in validated_data.new_tags],
            walking_distance=validated_data.walking_distance
        )
        
        return jsonify(ItemResponse.model_validate(item).model_dump()), 201
    
    except ValidationError as e:
        # Convert errors to ensure all values are JSON serializable
        errors = []
        for error in e.errors():
            serializable_error = {
                'loc': error['loc'],
                'msg': error['msg'],
                'type': error['type']
            }
            if 'ctx' in error:
                # Convert context values to strings if they're not serializable
                serializable_error['ctx'] = {k: str(v) for k, v in error['ctx'].items()}
            errors.append(serializable_error)
        
        return jsonify({
            'message': 'Validation error',
            'errors': errors
        }), 400
    
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    
    except Exception as e:
        # Log the error in production
        return jsonify({'message': 'An error occurred while creating item'}), 500


@item_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_items():
    """
    Get all items.
    
    Returns:
        200: List of all items
        500: Internal server error
    """
    try:
        items = _item_service.get_all_items()
        return jsonify([ItemResponse.model_validate(item).model_dump() for item in items]), 200
    
    except Exception as e:
        # Log the error in production
        return jsonify({'message': 'An error occurred while fetching items'}), 500


@item_bp.route('/<int:item_id>', methods=['GET'])
@jwt_required()
def get_item_by_id(item_id):
    """
    Get item by ID.
    
    Args:
        item_id: ID of the item to retrieve
    
    Returns:
        200: Item details
        404: Item not found
        500: Internal server error
    """
    try:
        item = _item_service.get_item_by_id(item_id)
        return jsonify(ItemResponse.model_validate(item).model_dump()), 200
    
    except ValueError as e:
        return jsonify({'message': str(e)}), 404
    
    except Exception as e:
        # Log the error in production
        return jsonify({'message': 'An error occurred while fetching item'}), 500
