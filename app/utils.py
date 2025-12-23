from functools import wraps
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from flask import jsonify

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            # Token oluştururken role bilgisini eklemiştik (auth_routes.py içinde)
            if claims.get("role") != "admin":
                return jsonify({"message": "Admins only!"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper