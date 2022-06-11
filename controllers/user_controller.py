from flask import request, Response
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from services.user_service import add_user, update_user, delete_user, get_user, get_all_users
from errors import SchemaValidationError, UserAlreadyExistsError, InternalServerError, UpdatingUserError, \
    DeletingUserError, UserNotExistsError


class UsersApi(Resource):

    @jwt_required()
    def get(self):
        users = get_all_users()
        return Response(users, mimetype="application/json", status=200)

    @jwt_required()
    def post(self):
        try:
            body = request.get_json()
            user_data = dict()
            user_data['email'] = body['email']
            user_data['password'] = body['password']
            user_data['name'] = body['name']
            user_data['role'] = body['role']
            obj_id = add_user(user_data)
            return {'success': f"Created book with id {obj_id}"}, 200
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except NotUniqueError:
            raise UserAlreadyExistsError
        except Exception:
            raise InternalServerError


class UserApi(Resource):

    @jwt_required()
    def put(self, obj_id):
        try:
            body = request.get_json()
            user_data = dict()
            user_data['email'] = body['email']
            user_data['name'] = body['name']
            user_data['role'] = body['role']
            updated_data = update_user(obj_id, user_data)
            return updated_data, 200
        except InvalidQueryError:
            raise SchemaValidationError
        except DoesNotExist:
            raise UpdatingUserError
        except Exception:
            raise InternalServerError

    @jwt_required()
    def delete(self, obj_id):
        try:
            delete_user(obj_id)
            return 'success', 200
        except DoesNotExist:
            raise UserNotExistsError
        except Exception:
            raise DeletingUserError

    @jwt_required()
    def get(self, obj_id):
        try:
            user = get_user(obj_id)
            return Response(user, mimetype="application/json", status=200)
        except DoesNotExist:
            raise UserNotExistsError
        except Exception:
            raise InternalServerError
