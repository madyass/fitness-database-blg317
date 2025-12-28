from flask import Blueprint, request, jsonify
from app.models.user_dao import create_user, get_user_by_username
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Registers a new user.
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      201:
        description: User registered successfully
      400:
        description: An error occurred
    """
    data = request.get_json()
    
    # Note: In a real project, you should hash the password (e.g. werkzeug.security)
    # Saving as plain text for now.
    try:
        user_id = create_user(data['username'], data['password'])
        return jsonify({"message": "User registered", "id": user_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Logs in and returns a JWT Token.
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: Token generated successfully
      401:
        description: Invalid username or password
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = get_user_by_username(username)
    
    # Password check (Simple string comparison)
    if user and user['password'] == password:
        # Create Token
        # cast user['id'] to str
        access_token = create_access_token(identity=str(user['id']), additional_claims={"role": user['role']})
        return jsonify(access_token=access_token), 200
    
    return jsonify({"message": "Invalid credentials"}), 401