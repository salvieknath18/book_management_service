from flask_restful import Api
from errors import errors
from routes import initialize_routes



def initialize_api(app):
    api = Api(app, errors=errors)
    app.config.from_envvar('ENV_FILE_LOCATION')

    initialize_routes(api)
