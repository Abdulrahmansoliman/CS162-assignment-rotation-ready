from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.item import Item
from app.models.category_item import CategoryItem
from app.models.item_tag_value import ItemTagValue
from app.models.value import Value
from app.models.tag import Tag
from app.models.category import Category
from app.models.user import User
from app.api.v1.schemas.item_schema import ItemResponse, CategoryResponse, TagValueResponse
from app import db
from sqlalchemy.orm import joinedload

item_bp = Blueprint('item', __name__)

def serialize_item(item):
    """Serialize item with categories and tags"""
    # Get categories
    categories = []
    for category_item in item.category_items:
        categories.append(CategoryResponse(
            category_id=category_item.category.category_id,
            name=category_item.category.name,
            pic=category_item.category.pic
        ))
    
    # Get tags
    tags = []
    for item_tag_value in item.item_tag_values:
        value = item_tag_value.value
        tag = value.tag
        
        tag_value = None
        boolean_value = None
        
        if value.boolean_val is not None:
            boolean_value = value.boolean_val
        elif value.name_val:
            tag_value = value.name_val
        elif value.numerical_value is not None:
            tag_value = str(value.numerical_value)
        
        tags.append(TagValueResponse(
            tag_name=tag.name,
            value=tag_value,
            boolean_value=boolean_value
        ))
    
    return ItemResponse(
        item_id=item.item_id,
        name=item.name,
        location=item.location,
        walking_distance=item.walking_distance,
        number_of_verifications=item.number_of_verifications,
        last_verified_date=item.last_verified_date,
        categories=categories,
        tags=tags
    )

@item_bp.route('/', methods=['GET'])
@jwt_required()
def get_items():
    """Get items for the current user's rotation city"""
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    
    if not user or not user.rotation_city_id:
        return jsonify({'message': 'User or rotation city not found.'}), 404
    
    # Get query parameters
    category_id = request.args.get('category_id', type=int)
    search_query = request.args.get('search', type=str)
    
    # Build query
    query = db.session.query(Item).filter_by(rotation_city_id=user.rotation_city_id)
    
    # Filter by category if provided
    if category_id:
        query = query.join(CategoryItem).filter(CategoryItem.category_id == category_id)
    
    # Filter by search query if provided
    if search_query:
        query = query.filter(
            db.or_(
                Item.name.ilike(f'%{search_query}%'),
                Item.location.ilike(f'%{search_query}%')
            )
        )
    
    items = query.options(
        joinedload(Item.category_items).joinedload(CategoryItem.category),
        joinedload(Item.item_tag_values).joinedload(ItemTagValue.value).joinedload(Value.tag)
    ).all()
    
    return jsonify([serialize_item(item).model_dump() for item in items]), 200

@item_bp.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    """Get all categories with item counts for current user's city"""
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    
    if not user or not user.rotation_city_id:
        return jsonify({'message': 'User or rotation city not found.'}), 404
    
    # Get all categories with counts
    categories = db.session.query(Category).all()
    result = []
    
    for category in categories:
        count = db.session.query(Item).join(CategoryItem).filter(
            CategoryItem.category_id == category.category_id,
            Item.rotation_city_id == user.rotation_city_id
        ).count()
        
        result.append({
            'category_id': category.category_id,
            'name': category.name,
            'pic': category.pic,
            'count': count
        })
    
    return jsonify(result), 200

