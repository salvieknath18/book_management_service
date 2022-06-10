def add_user(user_obj):
    user_obj.hash_password()
    user_obj.save()
    user_id = user_obj.user_id
    return user_id
