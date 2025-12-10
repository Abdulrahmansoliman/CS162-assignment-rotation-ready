"""
Category Routes
REST API endpoints for category CRUD operations.
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.services.category_service import CategoryService
from app.api.v1.schemas.category_schema import CategorySchemaResponse

category_bp = Blueprint('category', __name__)


@category_bp.route('/', methods=['GET'])
@jwt_required()
def get_categories():
    """Get all categories."""
    service = CategoryService()
    categories = service.get_all_categories()

    if not categories:
        return jsonify({'error': 'No categories found'}), 404

    return jsonify([CategorySchemaResponse.model_validate(cat).model_dump() for cat in categories]), 200


@category_bp.route('/<int:category_id>', methods=['GET'])
@jwt_required()
def get_category_by_id(category_id: int):
    """Get category by ID."""
    service = CategoryService()
    category = service.get_category_by_id(category_id)

    if not category:
        return jsonify({'error': 'Category not found'}), 404

    return jsonify(CategorySchemaResponse.model_validate(category).model_dump()), 200


@category_bp.route('/', methods=['POST'])
@jwt_required()
def add_category():
    """Create new category."""
    service = CategoryService()
    data = request.get_json()

    if not data or 'category_name' not in data or 'category_pic' not in data:
        return jsonify({'error': 'category_name and category_pic are required'}), 400

    category = service.add_category(
        category_name=data['category_name'],
        category_pic=data['category_pic']
    )

    if not category:
        return jsonify({'error': 'Failed to create category'}), 500

    return jsonify(CategorySchemaResponse.model_validate(category).model_dump()), 201


@category_bp.route('/<int:category_id>', methods=['PUT'])
@jwt_required()
def update_category(category_id: int):
    """Update category."""
    service = CategoryService()
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    category = service.update_category(
        category_id=category_id,
        category_name=data.get('category_name'),
        category_pic=data.get('category_pic')
    )

    if not category:
        return jsonify({'error': 'Category not found'}), 404

    return jsonify(CategorySchemaResponse.model_validate(category).model_dump()), 200