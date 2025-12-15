"""
Category Routes
REST API endpoints for category operations.
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.services.category_service import CategoryService
from app.api.v1.schemas.category_schema import CategorySchemaResponse

category_bp = Blueprint('category', __name__)

service = CategoryService()


@category_bp.route('/', methods=['GET'])
@jwt_required()
def get_categories():
    """Get all item categories.
    
    Returns all available categories for organizing items.
    
    Headers:
        Authorization: Bearer <access_token>
        
    Query Parameters:
        no_images (bool): If true, excludes category_pic from response
        
    Returns:
        200: List of categories
        404: No categories found
    """
    no_images = request.args.get('no_images', 'false').lower() == 'true'
    categories = service.get_all_categories()

    if not categories:
        return jsonify({'error': 'No categories found'}), 404

    if no_images:
        # Return categories without pictures
        return jsonify([
            {
                'category_id': cat.category_id,
                'category_name': cat.category_name
            }
            for cat in categories
        ]), 200

    return jsonify([
        CategorySchemaResponse.model_validate(cat).model_dump()
        for cat in categories
    ]), 200


@category_bp.route('/<int:category_id>', methods=['GET'])
@jwt_required()
def get_category_by_id(category_id: int):
    """Get a specific category by ID.
    
    Path Parameters:
        category_id (int): The ID of the category to retrieve
        
    Headers:
        Authorization: Bearer <access_token>
        
    Query Parameters:
        no_images (bool): If true, excludes category_pic from response
        
    Returns:
        200: Category information
        404: Category not found
    """
    no_images = request.args.get('no_images', 'false').lower() == 'true'
    category = service.get_category_by_id(category_id)

    if not category:
        return jsonify({'error': 'Category not found'}), 404

    if no_images:
        return jsonify({
            'category_id': category.category_id,
            'category_name': category.category_name
        }), 200

    return jsonify(
        CategorySchemaResponse.model_validate(category).model_dump()
    ), 200


# @category_bp.route('/', methods=['POST'])
# @jwt_required()
# def add_category():
#     """Create new category - NOT SUPPORTED."""
#     pass

# @category_bp.route('/<int:category_id>', methods=['PUT'])
# @jwt_required()
# def update_category(category_id: int):
#     """Update category - NOT SUPPORTED."""
#     pass
