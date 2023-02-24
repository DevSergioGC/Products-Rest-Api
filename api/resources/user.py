from flask_smorest import Blueprint

blp = Blueprint("users", __name__, url_prefix="/users", description="Operations on users")