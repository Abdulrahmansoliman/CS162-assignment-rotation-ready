from flask import Blueprint, jsonify
from pydantic import BaseModel


verification_bp = Blueprint('verification', __name__, url_prefix='/api/v1/verification')


class VerificationResponse(BaseModel):
    """Response schema for verification"""
    verification_id: int
    user_id: int
    status: str
    created_at: str
    updated_at: str


@verification_bp.route('/<int:verification_id>', methods=['GET'])
def get_verification(verification_id):
    """Get verification by verification id"""
    verifications = []  # TODO: query the database for the verification by id

    return jsonify({'verification': [VerificationResponse(
        verification_id=verification.verification_id,
        user_id=verification.user_id,
        status=verification.status,
        created_at=verification.created_at,
        updated_at=verification.updated_at
    ).model_dump() for verification in verifications]})