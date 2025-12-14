"""Item endpoints."""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from pydantic import ValidationError

from app.services.item_service import ItemService
from app.services.user_service import UserService
from app.api.v1.schemas.item_schema import CreateItemRequest, ItemResponse

item_bp = Blueprint('item', __name__)

_item_service = ItemService()
_user_service = UserService()


@item_bp.route('/', methods=['POST'])
@jwt_required()
def create_item():
    """Create a new item with categories and tags.
    
    Headers:
        Authorization: Bearer <access_token>
    
    Request Body:
        name (str): Item name
        location (str): Item location
        walking_distance (float, optional): Walking distance in meters
        category_ids (list[int]): List of category IDs (at least one required)
        existing_tags (list[dict]): List of {tag_id, value} for existing tags
        new_tags (list[dict]): List of {name, value_type, value} for new tags
    
    Returns:
        201: Item created successfully
        400: Validation error or user has no rotation city
        500: Internal server error
    """
    user_id = get_jwt_identity()
    
    # Validate request body exists
    if not request.json:
        return jsonify({'message': 'Request body is required'}), 400
    
    try:
        # Validate input with Pydantic
        validated_data = CreateItemRequest(**request.json)
        
        # Get user's rotation_city_id
        user = _user_service.get_user_by_id(user_id)
        
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
    """Get all items for the current user's rotation city.
    
    Returns all items shared by students in the authenticated user's city,
    with full details including categories, tags, and values.
    
    Headers:
        Authorization: Bearer <access_token>
    
    Returns:
        200: List of items in user's rotation city
        400: User has no rotation city assigned
        500: Internal server error
    """
    try:
        # Get user's rotation_city_id
        user_id = get_jwt_identity()
        user = _user_service.get_user_by_id(user_id)
        
        if not user or not user.rotation_city_id:
            return jsonify({'message': 'User has no rotation city assigned'}), 400
        
        # Get items filtered by rotation city with full details
        items = _item_service.get_all_items_with_details(user.rotation_city_id)
        return jsonify([ItemResponse.model_validate(item).model_dump() for item in items]), 200
    
    except Exception as e:
        # Log the error in production
        return jsonify({'message': 'An error occurred while fetching items'}), 500
Get item by ID (must belong to user's rotation city).
    
    Returns full item details including categories, tags, and values.
    Only returns items that belong to the user's rotation city.
    
    Path Parameters:
        item_id (int): ID of the item to retrieve
        
    Headers:
        Authorization: Bearer <access_token>
    
    Returns:
        200: Item details with all relationships loaded
    Args:
        item_id: ID of the item to retrieve
    
    Returns:
        200: Item details
        400: User has no rotation city assigned
        404: Item not found or doesn't belong to user's rotation city
        500: Internal server error
    """
    try:
        # Get user's rotation_city_id
        user_id = get_jwt_identity()
        user = _user_service.get_user_by_id(user_id)
        
        if not user or not user.rotation_city_id:
            return jsonify({'message': 'User has no rotation city assigned'}), 400
        
        # Get item filtered by rotation city with full details
        item = _item_service.get_item_by_id_with_details(item_id, user.rotation_city_id)
        return jsonify(ItemResponse.model_validate(item).model_dump()), 200
    
    except ValueError as e:
        return jsonify({'message': str(e)}), 404
    
    except Exception as e:
        # Log the error in production
        return jsonify({'message': 'An error occurred while fetching item'}), 500
