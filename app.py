from flask import Flask
from flask_smorest import Api
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from api.db import db

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
    migrate = Migrate(app, db)
    api = Api(app)
    
    #? API Configuration 
    
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(ProductBlueprint)
    api.register_blueprint(JWTBlueprint)
    api.register_blueprint(LoginBlueprint)
    api.register_blueprint(LevelBlueprint)
    
    return app