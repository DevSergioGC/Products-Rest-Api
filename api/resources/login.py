from flask.views import MethodView
from flask_smorest import Blueprint, abort
from api.schemas import UserSchema
from passlib.hash import pbkdf2_sha256 as hasher
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, create_refresh_token, get_jwt_identity
import datetime
from sqlalchemy import or_
from api.models import UserModel, JWTModel

blp = Blueprint("login", __name__, description="Operations on Login/Logout/Register")

@blp.route("/register")
class UserList(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, new_data):
        """Create a new user"""
        if UserModel.query.filter(
            or_(
                UserModel.username == new_data["username"],
                UserModel.email == new_data["email"]
            )
        ).first():
            abort(409, message="Username or email already exists")
        
        user = UserModel(
            username = new_data["username"],
            email = new_data["email"],
            password= hasher.hash(new_data["password"]),
            level_id = new_data["level_id"]
        )
        user.save_to_db()
        
        return {"message": "User created successfully"}, 201

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    # @blp.response(200, UserSchema)
    def post(self, new_data):
        """Login a user"""
        user = UserModel.query.filter_by(username=new_data["username"]).first()
        
        if user and hasher.verify(new_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True, expires_delta=datetime.timedelta(minutes=30))
            refresh_token = create_refresh_token(identity=user.id)
            
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 200
            
        else:
            return {"message": "Invalid credentials"}, 401

@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        """Refresh a token"""
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        jti = JWTModel(jti=get_jwt()["jti"])
        jti.save_to_db()
        
        return {"access_token": new_token}, 200      

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        """Logout a user"""
        jti = JWTModel(jti=get_jwt()["jti"])
        jti.save_to_db()
        
        return {"message": "Successfully logged out"}, 200