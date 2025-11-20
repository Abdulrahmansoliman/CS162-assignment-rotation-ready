from flask import Blueprint, jsonify
from pydantic import BaseModel
from typing import Optional


categories_bp = Blueprint('categories', __name__, url_prefix='/api/v1/categories')


class CategoriesResponse(BaseModel):
    """Response from calling the category"""
    category_id: str
    category_name: str
    category_pic: Optional[str] = None  # TODO: support pictures


@categories_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get the categories for filtering"""
    categories = []

    return jsonify(
        {'categories': [CategoriesResponse(
            category_id=category.category_id,
            category_name=category.category_name,
            category_pic=category.category_pic).
            model_dump()
            for category in categories]}
    )