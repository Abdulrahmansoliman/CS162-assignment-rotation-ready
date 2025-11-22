from flask import Blueprint, jsonify
from pydantic import BaseModel
from typing import Optional
from app.services.category_service import CategoryService

categories_bp = Blueprint('categories', __name__, url_prefix='/api/v1/categories')


@categories_bp.route('/', methods=['GET'])
def get_categories():
    """Get the categories for filtering"""
    categories = CategoryService.get_all_categories()

    if not categories:
        return jsonify({"error": "Categories not found"}), 404

    category_data = [category.name for category in categories]

    return jsonify(category_data), 200