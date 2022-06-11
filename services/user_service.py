from models.user import User
from flask_jwt_extended import get_jwt_identity, jwt_required


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
