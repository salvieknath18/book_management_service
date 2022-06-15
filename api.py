from flask_restful import Api
from errors import errors
from routes import initialize_routes
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint


def initialize_api(app):
    api = Api(app, errors=errors)
    app.config.from_envvar('ENV_FILE_LOCATION')
    swagger_url = '/swagger'
    api_url = '/static/swagger.yml'
    swagger_ui_blueprint = get_swaggerui_blueprint(
        swagger_url,
        api_url,
        config={'app_name': "Book Management Portal"}
    )

    CORS(app)
    Bcrypt(app)
    JWTManager(app)
    app.register_blueprint(swagger_ui_blueprint, url_prefix=swagger_url)
    initialize_routes(api)
