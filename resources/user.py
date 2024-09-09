from flask.views import MethodView
from flask_smorest import Blueprint, abort
from jinja2.runtime import identity
from passlib.hash import pbkdf2_sha256 #will hash the password
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity,jwt_required, get_jwt

from db import db
from blocklist import BLOCKLIST
from models import UserModel
from schemas import UserSchema


blp = Blueprint("Users", "users", description="Operations on users")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username== user_data["username"]).first():
            abort(409, message="A user with that username already exists")

        # alter the password string before saving the data
        user = UserModel(
            username = user_data["username"],
            password = pbkdf2_sha256.hash(user_data["password"])
        )
        db.session.add(user)
        db.session.commit()
        return {"message": "User created successfully."}, 201
    

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        #get back the user with a matching username
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()
        
        #check if a user was returned and the passwords are the same using .verify()
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}
        abort(401, message="Invalid Credentials")


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()  #return None if now new current user
        new_token = create_access_token(identity=current_user, fresh=False)
        jti = get_jwt()["jti"]   # a created non-fresh access token cannot be used again
        BLOCKLIST.add(jti)  #add the jti to the blocklist
        return {"access_token": new_token}



@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        #when logging out, we want to put the access token in the blocklist
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out "}


@blp.route("/user/<int:user_id>")
class User(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}, 200