from flask.views import MethodView
from flask_smorest import Blueprint, abort
from api.schemas import LevelSchema
from flask_jwt_extended import get_jwt, jwt_required, get_jwt_identity
from api.models import LevelModel

blp = Blueprint("level", __name__, description="Operations on Levels")

@blp.route("/level")
class LevelList(MethodView):
    @blp.arguments(LevelSchema)
    @blp.response(201, LevelSchema)
    # @jwt_required()
    def post(self, new_data):
        """Create a new level"""
        if LevelModel.query.filter(
            LevelModel.name == new_data["name"]
        ).first():
            abort(409, message="Level already exists")
        
        level = LevelModel(
            name = new_data["name"],
        )
        level.save_to_db()
        
        return {"message": "Level created successfully"}, 201
    
    def get(self):
        """Get all levels"""
        return LevelModel.query.all()