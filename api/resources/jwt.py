from flask_smorest import Blueprint

blp = Blueprint("jwt", __name__, url_prefix="/jwt", description="Operations on Revoked JWT")