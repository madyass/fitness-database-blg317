from flask import Blueprint, request, jsonify
from app.models.member_dao import create_member, get_all_members, update_member, delete_member
from flask_jwt_extended import jwt_required 
from app.utils import admin_required
member_bp = Blueprint('member', __name__)

@member_bp.route('/', methods=['POST'])
@jwt_required()
def add_new_member():
    """
    Registers a new member.
    ---
    tags:
      - Members
    security:
      - Bearer: []
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
            email:
              type: string
            plan_id:
              type: integer
    responses:
      201:
        description: Member created
    """
    data = request.get_json()
    try:
        mid = create_member(
            data['first_name'], 
            data['last_name'], 
            data['email'], 
            data['plan_id']
        )
        return jsonify({"message": "Member created", "member_id": mid}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

@member_bp.route('/', methods=['GET'])
@jwt_required()
def list_members():
    """
    Lists all members.
    ---
    tags:
      - Members
    responses:
      200:
        description: List of members
    """
    members = get_all_members()
    return jsonify(members), 200

@member_bp.route('/<int:member_id>', methods=['PUT'])
@jwt_required()
def edit_member(member_id):
    """
    Updates member information.
    ---
    tags:
      - Members
    parameters:
      - name: member_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        schema:
            properties:
                phone: {type: string}
                address: {type: string}
    responses:
      200:
        description: Member updated
    """
    data = request.get_json()
    update_member(member_id, data.get('phone'), data.get('address'))
    return jsonify({"message": "Member updated"}), 200

@member_bp.route('/<int:member_id>', methods=['DELETE'])
@admin_required()
def remove_member(member_id):
    """
    Deletes a member.
    ---
    tags:
      - Members
    parameters:
      - name: member_id
        in: path
        type: integer
        required: true  
    responses:
      200:
        description: Member deleted
    """
    delete_member(member_id)
    return jsonify({"message": "Member deleted"}), 200