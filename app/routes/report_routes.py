from flask import Blueprint, jsonify
from app.models.report_dao import get_inactive_members_report, get_coach_retention_report
from flask_jwt_extended import jwt_required

report_bp = Blueprint('report', __name__)

@report_bp.route('/inactive-members', methods=['GET'])
@jwt_required()
def inactive_members():
    """
    Lists active members with absenteeism (Complex Query).
    ---
    tags:
      - Reports
    security:
      - Bearer: []
    responses:
      200:
        description: Returns list of members
    """
    try:
        data = get_inactive_members_report()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@report_bp.route('/coach-analysis', methods=['GET'])
@jwt_required()
def coach_analysis():
    """
    Analyzes instructor student retention rates.
    ---
    tags:
      - Reports
    security:
      - Bearer: []
    responses:
      200:
        description: Instructor analysis report
    """
    try:
        data = get_coach_retention_report()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500