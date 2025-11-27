from flask import jsonify, Blueprint
from app.services.category_service import CategoryService
from app.api.v1.schemas.responses import CategoryResponse


category_bp = Blueprint('category', __name__)


@category_bp.route('/', methods=['GET'])
def get_category():
    pass