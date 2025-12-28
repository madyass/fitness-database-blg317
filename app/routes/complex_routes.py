from flask import Blueprint, jsonify
from app.models.complex_dao import (
    get_popular_classes,
    get_peak_hours,
    get_revenue_by_plan,
    get_instructor_performance,
    get_maintenance_costs
)
from flask_jwt_extended import jwt_required

complex_bp = Blueprint('complex', __name__)

@complex_bp.route('/popular-classes', methods=['GET'])
# @jwt_required() # Optional: Uncomment if protection is needed
def popular_classes():
    """
    Lists classes ordered by popularity (enrollment count).
    ---
    tags:
      - Analytics
    responses:
      200:
        description: List of popular classes
    """
    try:
        data = get_popular_classes()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@complex_bp.route('/peak-hours', methods=['GET'])
def peak_hours():
    """
    Returns peak hours based on class attendance.
    ---
    tags:
      - Analytics
    responses:
      200:
        description: List of peak hours
    """
    try:
        data = get_peak_hours()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@complex_bp.route('/revenue-by-plan', methods=['GET'])
def revenue_by_plan():
    """
    Returns total revenue broken down by membership plan.
    ---
    tags:
      - Analytics
    responses:
      200:
        description: Revenue by plan
    """
    try:
        data = get_revenue_by_plan()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@complex_bp.route('/instructor-performance', methods=['GET'])
def instructor_performance():
    """
    Returns instructor performance metrics (Class size + Private sessions).
    ---
    tags:
      - Analytics
    responses:
      200:
        description: Instructor performance report
    """
    try:
        data = get_instructor_performance()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@complex_bp.route('/maintenance-costs', methods=['GET'])
def maintenance_costs():
    """
    Returns total maintenance costs by equipment category.
    ---
    tags:
      - Analytics
    responses:
      200:
        description: Maintenance costs report
    """
    try:
        data = get_maintenance_costs()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
