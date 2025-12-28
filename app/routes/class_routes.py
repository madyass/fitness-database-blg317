from flask import Blueprint, request, jsonify
from app.models.class_dao import get_all_classes, create_group_class
from flask_jwt_extended import jwt_required

class_bp = Blueprint('class', __name__)

@class_bp.route('/', methods=['GET'])
def list_classes():
    """
    Lists all group classes.
    ---
    tags:
      - Classes
    responses:
      200:
        description: Returns list of classes
    """
    return jsonify(get_all_classes()), 200

@class_bp.route('/', methods=['POST'])
@jwt_required()
def add_class():
    """
    Schedules a new group class.
    ---
    tags:
      - Classes
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            class_name:
              type: string
            instructor_id:
              type: integer
            room_id:
              type: integer
            start_time:
              type: string
              example: '2025-01-01 10:00:00'
    responses:
      201:
        description: Class created
    """
    data = request.get_json()
    new_id = create_group_class(
        data['class_name'], 
        data['instructor_id'], 
        data['room_id'], 
        data['start_time']
    )
    return jsonify({"message": "Class scheduled", "id": new_id}), 201
