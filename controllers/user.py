from flask import request, Response
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError

from models.user import User
from services.user import add_user
from errors import SchemaValidationError, UserAlreadyExistsError, InternalServerError, UpdatingUserError, \
    DeletingUserError, UserNotExistsError


class UsersApi(Resource):

    @staticmethod
    def get():
        users = User.objects().to_json()
        return Response(users, mimetype="application/json", status=200)

    @jwt_required
    def post(self):
        try:
            body = request.get_json()
            user = User(**body)
            user_id = add_user(user)
            return {'user_id': str(user_id)}, 200
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except NotUniqueError:
            raise UserAlreadyExistsError
        except Exception:
            raise InternalServerError


class UserApi(Resource):
    @jwt_required
    def put(self, user_id):
        try:
            # doc_id = get_jwt_identity()
            # user = User.objects().get(id=doc_id)
            body = request.get_json()
            User.objects.get(id=user_id).update(**body)
            return '', 200
        except InvalidQueryError:
            raise SchemaValidationError
        except DoesNotExist:
            raise UpdatingUserError
        except Exception:
            raise InternalServerError

    @jwt_required
    def delete(self, user_id):
        try:
            # doc_id = get_jwt_identity()
            user = User.objects().get(id=user_id)
            user.delete()
            return '', 200
        except DoesNotExist:
            raise UserNotExistsError
        except Exception:
            raise DeletingUserError

    @staticmethod
    def get(user_id):
        try:
            users = User.objects().get(user_id=user_id).to_json()
            return Response(users, mimetype="application/json", status=200)
        except DoesNotExist:
            raise UserNotExistsError
        except Exception:
            raise InternalServerError
