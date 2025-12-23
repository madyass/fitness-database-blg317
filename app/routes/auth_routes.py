from flask import Blueprint, request, jsonify
from app.models.user_dao import create_user, get_user_by_username
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Yeni kullanıcı kaydı oluşturur.
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
        description: Kullanıcı başarıyla oluşturuldu
      400:
        description: Hata oluştu
    """
    data = request.get_json()
    
    # Not: Gerçek projede şifreyi hash'leyerek kaydetmelisin (örn: werkzeug.security)
    # Şimdilik düz kaydediyoruz.
    try:
        user_id = create_user(data['username'], data['password'])
        return jsonify({"message": "User registered", "id": user_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Giriş yapar ve JWT Token döner.
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
        description: Token başarıyla üretildi
      401:
        description: Hatalı kullanıcı adı veya şifre
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = get_user_by_username(username)
    
    # Şifre kontrolü (Basit string karşılaştırma)
    if user and user['password'] == password:
        # Token oluştur
        # user['id'] sayısını str() içine aldık
        access_token = create_access_token(identity=str(user['id']), additional_claims={"role": user['role']})
        return jsonify(access_token=access_token), 200
    
    return jsonify({"message": "Invalid credentials"}), 401