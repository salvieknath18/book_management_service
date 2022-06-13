from flask import request, Response
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from services.user_service import add_user, update_user, delete_user, get_user, get_all_users, \
    clean_all_users, clean_user
from errors import SchemaValidationError, UserAlreadyExistsError, InternalServerError, UpdatingUserError, \
    DeletingUserError, UserNotExistsError
from services.user_service import roles_required
import json


class UsersApi(Resource):

    @jwt_required()
    @roles_required('admin')
    def get(self):
        users = get_all_users()
        users_data = clean_all_users(users)
        return Response(json.dumps(users_data), mimetype="application/json", status=200)

    @jwt_required()
    @roles_required('admin')
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
    @roles_required('admin')
    def put(self, id):
        try:
            body = request.get_json()
            user_data = dict()
            user_data['email'] = body['email']
            user_data['name'] = body['name']
            user_data['role'] = body['role']
            updated_user = update_user(id, user_data)
            updated_data = clean_user(updated_user)
            return Response(json.dumps(updated_data), mimetype="application/json", status=200)
        except InvalidQueryError:
            raise SchemaValidationError
        except DoesNotExist:
            raise UpdatingUserError
        except Exception:
            raise InternalServerError

    @jwt_required()
    @roles_required('admin')
    def delete(self, id):
        try:
            delete_user(id)
            return 'success', 200
        except DoesNotExist:
            raise UserNotExistsError
        except Exception:
            raise DeletingUserError

    @jwt_required()
    @roles_required('admin')
    def get(self, id):
        try:
            user = clean_user(get_user(id))
            return Response(json.dumps(user), mimetype="application/json", status=200)
        except DoesNotExist:
            raise UserNotExistsError
        except Exception:
            raise InternalServerError
