from flask import jsonify, Blueprint, request
from app.services.category_service import CategoryService
from app.api.v1.schemas.responses import CategoryResponse
from flask_jwt_extended import jwt_required


category_bp = Blueprint('category', __name__)


@category_bp.route('/', methods=['GET'])
def get_all_categories():
    """Get list of all categories"""
    service = CategoryService()

    categories = service.get_all_categories()

    if not categories:
        return jsonify({"error": "No categories found"}), 404

    return jsonify([CategoryResponse.model_validate(category).model_dump() for category in categories]), 200


@category_bp.route('/<int:category_id>', methods=['GET'])
def get_category_by_id(category_id):
    """Get category by category_id"""
    service = CategoryService()

    category = service.get_category_by_id(category_id)

    if not category:
        return jsonify({"error": "Category not found"}), 404

    return jsonify(CategoryResponse.model_validate(category).model_dump()), 200


@jwt_required()
@category_bp.route('/', methods=['POST'])
def add_category():
    """Add a new category"""

    service = CategoryService()
    data = request.get_json()

    if not data:
        return jsonify({'error':'Category name is required'}), 400
    
    category = service.add_category(
        category_name=data['category_name'],
        category_pic=data.get('category_pic'),
    )

    if not category:
        return jsonify({'error':'Failed to create category'}), 500
    
    return jsonify(CategoryResponse.model_validate(category).model_dump()), 201


@jwt_required()
@category_bp.route("/<int:category_id>", methods=['DELETE'])
def delete_category(category_id):
    """Delete category"""

    service = CategoryService()
    success = service.delete_category(category_id=category_id)

    if not success:
        return jsonify({'error':'Category not found'}), 404

    return jsonify("Category deleted successfully!"), 200


@jwt_required()
@category_bp.route("/<int:category_id>", methods=['PUT'])
def update_category(category_id):
    """Update category"""

    service = CategoryService()
    data = request.get_json()

    if not data:
        return jsonify({'error':'No data found'}), 404
    
    category = service.update_category(
        category_id=category_id,
        category_name=data.get('category_name'),
        category_pic=data.get('category_pic'),
    )

    if not category:
        return jsonify({'error':'Category failed to update'}), 404
    
    return jsonify(CategoryResponse.model_validate(category).model_dump()), 200