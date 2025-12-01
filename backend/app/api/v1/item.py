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
        return jsonify({
            'message': 'Validation error',
            'errors': e.errors()
        }), 400
    
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    
    except Exception as e:
        # Log the error in production
        return jsonify({'message': 'An error occurred while creating item'}), 500
