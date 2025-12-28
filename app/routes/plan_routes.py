from flask import Blueprint, request, jsonify
from app.models.plan_dao import create_plan, get_all_plans
from flask_jwt_extended import jwt_required

plan_bp = Blueprint('plan', __name__)

@plan_bp.route('/', methods=['POST'])
@jwt_required() # Only logged-in users can add plans
def add_plan():
    """
    Creates a new membership plan.
    ---
    tags:
      - Plans
    parameters:
      - name: body
        in: body
        schema:
            properties:
                plan_name: {type: string}
                monthly_fee: {type: number}
                duration_months: {type: integer}
    responses:
      201:
        description: Plan created
    """
    data = request.get_json()
    p_id = create_plan(data['plan_name'], data['monthly_fee'], data['duration_months'])
    return jsonify({"message": "Plan created", "id": p_id}), 201

@plan_bp.route('/', methods=['GET'])
def list_plans():
    """
    Lists all plans.
    ---
    tags:
      - Plans
    responses:
      200:
        description: Lists all plans
    """
    return jsonify(get_all_plans()), 200