import datetime

from flask import request
from models.user import User
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from mongoengine.errors import FieldDoesNotExist, DoesNotExist, NotUniqueError

from services.user import add_user
from errors import SchemaValidationError, InternalServerError, UnauthorizedError, EmailAlreadyExistsError


class RegisterApi(Resource):
    @staticmethod
    def post():
        try:
            body = request.get_json()
            user = User(**body)
            user_id = add_user(user)
            return {'user_id': str(user_id)}, 200
        except FieldDoesNotExist:
            raise SchemaValidationError
        except NotUniqueError:
            raise EmailAlreadyExistsError
        except Exception:
            raise InternalServerError


class LoginApi(Resource):
    @staticmethod
    def post():
        try:
            body = request.get_json()
            user = User.objects().get(email=body.get('email'))
            authorized = user.check_password(body.get('password'))
            if not authorized:
                return {'error': 'Email or password invalid'}, 401
            expires = datetime.timedelta(days=7)
            access_token = create_access_token(identity=str(user.id), expires_delta=expires)
            return {'token': access_token}, 200
        except (UnauthorizedError, DoesNotExist):
            raise UnauthorizedError
        except Exception:
            raise InternalServerError
