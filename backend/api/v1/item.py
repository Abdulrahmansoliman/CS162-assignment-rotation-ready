from flask import Blueprint, jsonify
from pydantic import BaseModel
from datetime import datetime

item_bp = Blueprint("item", __name__, url_prefix="/api/v1/item")


class ItemsResponse(BaseModel):
    item_id: int
    item_name: str
    item_location: str
    walking_distance: float
    last_verified: str
    added_by: int
    created_at: datetime
    number_of_verifications: int


@item_bp.route('/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Get item by item id"""
    items = []  # TODO: query the database for the item by id

    return jsonify({'item': [ItemsResponse(
        item_id=item.item_id,
        item_name=item.item_name,
        item_location=item.item_location,
        walking_distance=item.walking_distance,
        last_verified=item.last_verified_date,
        added_by=item.added_by,
        created_at=item.created_at,
        number_of_verifications=item.number_of_verifications
    ).model_dump() for item in items]})