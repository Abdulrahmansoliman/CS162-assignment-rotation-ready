from flask import Blueprint, jsonify, request
from app.services.item_service import ItemService
from app.api.v1.schemas.schemas import ItemResponse

item_bp = Blueprint("item", __name__, url_prefix="/api/v1/items")


@item_bp.route('/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Get item by item id"""

    item = ItemService.get_item(item_id=item_id)

    if not item:
        return jsonify({'error': 'Item not found'}), 404
    
    return jsonify(ItemResponse.from_orm(item).model_dump()), 200


@item_bp.route('/', methods=['GET'])
def get_items():
    """Get all items"""

    from app.models.item import Item

    items = Item.query.all()

    if not items:
        return jsonify({"error": "Items not found"}), 404

    items_data = [item.name for item in items]

    return jsonify(items_data), 200


@item_bp.route('/', methods=['POST'])
def create_item():
    """Create a new item"""
    
    data = request.get_json()
    
    # Validate required fields
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    
    required_fields = ['name', 'location', 'added_by_user_id']

    if missing := [f for f in required_fields if f not in data]:
        return jsonify({'error': f'Missing: {", ".join(missing)}'}), 400
    
    item = ItemService.create_item(
        name=data['name'],
        location=data['location'],
        added_by_user_id=data['added_by_user_id'],
        walking_distance=data.get('walking_distance')
    )
    
    return jsonify(ItemResponse.from_orm(item).model_dump()), 201