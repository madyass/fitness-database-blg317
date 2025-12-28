from flask import Blueprint, request, jsonify
from app.models.instructor_dao import get_all_instructors, create_instructor
from flask_jwt_extended import jwt_required

instructor_bp = Blueprint('instructor', __name__)

@instructor_bp.route('/', methods=['GET'])
@jwt_required()
def list_instructors():
    """
    Lists all instructors.
    ---
    tags:
      - Instructors
    responses:
      200:
        description: Returns list of instructors
    """
    return jsonify(get_all_instructors()), 200

@instructor_bp.route('/', methods=['POST'])
@jwt_required()
def add_instructor():
    """
    Adds a new instructor.
    ---
    tags:
      - Instructors
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            first_name:
              type: string
            last_name:
              type: string
            specialization:
              type: string
    responses:
      201:
        description: Instructor created
    """
    data = request.get_json()
    new_id = create_instructor(data['first_name'], data['last_name'], data['specialization'])
    return jsonify({"message": "Instructor created", "id": new_id}), 201
