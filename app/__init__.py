from flask import Flask, request
import logging
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from config import Config
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Logging Setup
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    @app.before_request
    def log_request_info():
        logger.info(f"Incoming Request: {request.method} {request.path}")
        logger.info(f"Headers: {request.headers}")
        if request.get_json(silent=True):
             logger.info(f"Body: {request.get_json()}")
    
    @app.after_request
    def log_response_info(response):
        logger.info(f"Response Status: {response.status}")
        return response


    CORS(app)
    CORS(app)
    # Initialize JWT
    jwt = JWTManager(app)

    # SWAGGER SETTINGS (Required for Authorize Button)
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Gym Management API",
            "description": "API Documentation",
            "version": "1.0.0"
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Token format: Bearer <token>"
            }
        },
        # Show lock icon on all endpoints by default
        "security": [
            {
                "Bearer": []
            }
        ]
    }

    swagger = Swagger(app, template=swagger_template)

    # Register Blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.plan_routes import plan_bp
    from app.routes.member_routes import member_bp
    from app.routes.report_routes import report_bp
    from app.routes.instructor_routes import instructor_bp
    from app.routes.class_routes import class_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(plan_bp, url_prefix='/api/plans')
    app.register_blueprint(member_bp, url_prefix='/api/members')
    app.register_blueprint(report_bp, url_prefix='/api/reports')
    app.register_blueprint(instructor_bp, url_prefix='/api/instructors')
    app.register_blueprint(class_bp, url_prefix='/api/classes')

    return app