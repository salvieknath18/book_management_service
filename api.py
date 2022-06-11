from flask_restful import Api
from errors import errors
from routes import initialize_routes
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS


def initialize_api(app):
    api = Api(app, errors=errors)
    app.config.from_envvar('ENV_FILE_LOCATION')

    CORS(app)
    Bcrypt(app)
    JWTManager(app)
    initialize_routes(api)
