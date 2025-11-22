from flask import Blueprint, jsonify
from pydantic import BaseModel
from app.models.item_verification import ItemVerification


verification_bp = Blueprint('verification', __name__, url_prefix='/api/v1/verification')


class VerificationResponse(BaseModel):
    """Response schema for verification"""
    verification_id: int
    item_id: int
    user_id: int
    status: str
    notes: str | None = None

    class Config:
        from_attributes = True


@verification_bp.route('/<int:verification_id>', methods=['GET'])
def get_verification(verification_id):
    """Get verification by verification id"""
    verification = ItemVerification.query.filter_by(verification_id=verification_id).first()

    if not verification:
        return jsonify({"error": "Verification not found"}), 404

    return jsonify(VerificationResponse.model_validate(verification).model_dump()), 200
