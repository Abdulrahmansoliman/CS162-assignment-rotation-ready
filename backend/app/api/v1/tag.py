"""Tag endpoints."""
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from app.services.tag_service import TagService
from app.api.v1.schemas.tag_schema import TagResponse

tag_bp = Blueprint('tag', __name__)

_tag_service = TagService()


@tag_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_tags():
    """
    Get all available tags.
    
    Returns:
        200: List of all tags with their value types
    """
    tags = _tag_service.get_all_tags()
    
    return jsonify([
        TagResponse.model_validate(tag).model_dump()
        for tag in tags
    ]), 200
