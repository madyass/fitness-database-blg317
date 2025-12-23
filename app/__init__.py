from flask import Flask
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # JWT Başlat
    jwt = JWTManager(app)

    # SWAGGER AYARLARI (Authorize Butonu İçin Şart)
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Gym Management API",
            "description": "API Dokümantasyonu",
            "version": "1.0.0"
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Token formatı: Bearer <token>"
            }
        },
        # Tüm endpointlerde kilit ikonunu varsayılan olarak göster
        "security": [
            {
                "Bearer": []
            }
        ]
    }

    swagger = Swagger(app, template=swagger_template)

    # Blueprint'leri Kaydet
    from app.routes.auth_routes import auth_bp
    from app.routes.plan_routes import plan_bp
    from app.routes.member_routes import member_bp
    from app.routes.report_routes import report_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(plan_bp, url_prefix='/api/plans')
    app.register_blueprint(member_bp, url_prefix='/api/members')
    app.register_blueprint(report_bp, url_prefix='/api/reports')

    return app