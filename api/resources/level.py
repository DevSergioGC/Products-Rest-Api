from flask.views import MethodView
from flask_smorest import Blueprint, abort
from api.schemas import LevelSchema
from flask_jwt_extended import get_jwt, jwt_required, get_jwt_identity
from api.models import LevelModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("level", __name__, description="Operations on Levels")

@blp.route("/level")
class LevelList(MethodView):
    @blp.arguments(LevelSchema)
    @blp.response(201, LevelSchema)
    @jwt_required()
    def post(self, new_data):
        if get_jwt()["is_admin"] == False:
            abort(401, message="You are not authorized to create a new level")
        
        """Create a new level"""
        if LevelModel.query.filter(
            LevelModel.name == new_data["name"]
        ).first():
            abort(409, message="Level already exists")
        
        level = LevelModel(
            name = new_data["name"],
        )
        
        try:
            level.save_to_db()
        except IntegrityError:
            abort(409, message="Level already exists")
        except SQLAlchemyError:
            abort(500, message="Something went wrong while inserting the level")
        
        return level, 201
    
    @blp.response(200, LevelSchema(many=True))
    def get(self):
        """Get all levels"""
        return LevelModel.query.all()