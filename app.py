from flask import Flask, jsonify
from flask_smorest import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
from api.db import db
from api.models import RevokedJWTModel, UserModel

#? Import Blueprints
from api.resources.user import blp as UserBlueprint
from api.resources.product import blp as ProductBlueprint
from api.resources.jwt import blp as JWTBlueprint
from api.resources.login import blp as LoginBlueprint
from api.resources.level import blp as LevelBlueprint

def create_app():
    app = Flask(__name__)    
    load_dotenv()
    
    #? Flask-RESTX configuration
    
    app.config["API_TITLE"] = "Products REST API" # set api title
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    
    db.init_app(app) # initialize database
    migrate = Migrate(app, db, render_as_batch=True)
    api = Api(app)
    
    #? Flask-JWT-Extended configuration
    
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "super-secret")
    jwt = JWTManager(app)
    
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        jti = RevokedJWTModel.query.filter(RevokedJWTModel.jti == jwt_payload["jti"]).first()
        return True if jti else False
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return(
            jsonify(
                {
                    "description": "The token has been revoked.",
                    "error": "token_revoked"
                }
            )
        )
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return(
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required"
                }
            )
        )
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return(
            jsonify({"message": "The token has expired.", "error": "token_expired"}), 401
        )
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return(
            jsonify({"message": "Signature verification failed..", "error": "invalid_token"}), 401
        )
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return(
            jsonify({
                "description": "Request does not contain an access token.", 
                "error": "authorization_required"
            }), 401
        )
    
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        user = UserModel.find_by_id(identity)
        
        if user.level_id == 1:
            return {"is_admin": True}
        return {"is_admin": False}
    
    #? API Configuration 
    
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(ProductBlueprint)
    api.register_blueprint(JWTBlueprint)
    api.register_blueprint(LoginBlueprint)
    api.register_blueprint(LevelBlueprint)
    
    return app