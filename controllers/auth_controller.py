import datetime
import json
from flask import request, Response
from models.user import User
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from mongoengine.errors import FieldDoesNotExist, DoesNotExist, NotUniqueError

from services.user_service import add_user, clean_user
from errors import SchemaValidationError, InternalServerError, UnauthorizedError, EmailAlreadyExistsError


class RegisterApi(Resource):

    @staticmethod
    def post():
        try:
            body = request.get_json()
            user_data = dict()
            user_data['email'] = body['email']
            user_data['password'] = body['password']
            user_data['name'] = body['name']
            user_data['role'] = body['role']
            obj_id = add_user(user_data)
            return {'success': f"Created book with id {obj_id}"}, 200
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
            user_data = clean_user(user)
            user_data['token'] = access_token
            return Response(json.dumps(user_data), mimetype="application/json", status=200)
        except (UnauthorizedError, DoesNotExist):
            raise UnauthorizedError
        except Exception:
            raise InternalServerError
