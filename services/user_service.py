from models.user import User
from errors import InternalServerError
from flask_jwt_extended import get_jwt_identity
from functools import wraps


def roles_required(*role_names):
    """
    Decorator to address role base authorization
    :param role_names: list of roles allowed
    :return: raise error if role is not allowed else implement the inner function
    """
    def decorator(original_route):
        @wraps(original_route)
        def decorated_route(*args, **kwargs):
            user_id = get_jwt_identity()
            current_user = User.objects().get(id=user_id)
            if current_user.role not in role_names:
                raise InternalServerError
            else:
                return original_route(*args, **kwargs)
        return decorated_route
    return decorator


def add_user(user_data):
    """
    Functional block to address user addition logic
    :param user_data: User data required to create user in DB
    :return:
    """
    user = User(**user_data)
    user.hash_password()
    user.save()
    return user.id


def update_user(obj_id, user_data):
    user = User.objects.get(id=obj_id)
    user_data["password"] = user.password
    user.update(**user_data)
    return User.objects.get(id=obj_id).to_json()


def delete_user(obj_id):
    book = User.objects.get(id=obj_id)
    book.delete()


def get_user(obj_id):
    return User.objects.get(id=obj_id).to_json()


def get_all_users():
    return User.objects().to_json()


def get_current_user():
    user_id = get_jwt_identity()
    current_user = User.objects().get(id=user_id)
    return current_user
