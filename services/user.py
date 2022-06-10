
def add_user(user_obj):
    """
    Functional block to address user addition logic
    :param user_obj: User object which need to be created in DB
    :return:
    """
    user_obj.hash_password()
    user_obj.save()
    user_id = user_obj.user_id
    return user_id
