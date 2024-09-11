import os
import secrets
from dotenv import load_dotenv

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager #do pip install -r requirements.txt
from flask_migrate import Migrate

import models

from db import db
from blocklist import BLOCKLIST

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBluePrint

# from datetime import timedelta


def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    #for the SQLAlchemy database connection
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
        # Define security scheme for Swagger
    app.config["OPENAPI"] = {
        "components": {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT"
                }
            }
        },
        "security": [
            {
                "bearerAuth": []
            }
        ]
    }
    
    
    db.init_app(app)
    migrate = Migrate(app, db)
    
    api = Api(app)
    
    app.config["JWT_SECRET_KEY"] = str(secrets.SystemRandom().getrandbits(128)) #ex: 269254914869209016615852499953798428692
    # app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=300)  # Access token expiry

    jwt = JWTManager(app)

    #
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST
        #returns true, if the request is terminated; if the token is in the blocklist

    #this returns the error message that will be sent to the client when the token is revoked(the above function returns true)
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"description": "The token has been revoked.", "error": "token_revoked"}),
            401,
        )
    
    #adding more claims to the JWT. Does this when the JWT is created vs when it is called
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        #HERE you look into the database and see if the user is an admin
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    # JWT FUNCTIONS FOR ERROR HANDLING WHEN CALLING ENDPOINTS WITH JWT_REQUIRED -----------------
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    # JWT configuration ends -------------------------------------
    
    # with app.app_context():
    #     import models
    #     db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBluePrint)

    return app