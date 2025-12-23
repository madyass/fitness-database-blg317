from flask import Blueprint, jsonify
from app.models.report_dao import get_inactive_members_report
from flask_jwt_extended import jwt_required

report_bp = Blueprint('report', __name__)

@report_bp.route('/inactive-members', methods=['GET'])
@jwt_required()
def inactive_members():
    """
    Devamsızlık yapan aktif üyeleri listeler (Complex Query).
    ---
    tags:
      - Reports
    security:
      - Bearer: []
    responses:
      200:
        description: Üye listesi döner
    """
    try:
        data = get_inactive_members_report()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500