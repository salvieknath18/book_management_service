from controllers.user import UsersApi, UserApi


def initialize_routes(api):

    # Routing for User apis
    api.add_resource(UsersApi, '/api/users')
    api.add_resource(UserApi, '/api/users/<id>')
