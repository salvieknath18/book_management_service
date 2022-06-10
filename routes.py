from controllers.book import BooksApi, BookApi
from controllers.user import UsersApi, UserApi
from controllers.auth import RegisterApi, LoginApi


def initialize_routes(api):
    # Routing for books apis
    api.add_resource(BooksApi, '/api/books')
    api.add_resource(BookApi, '/api/books/<id>')

    # Routing for User apis
    api.add_resource(UsersApi, '/api/users')
    api.add_resource(UserApi, '/api/users/<id>')

    # Routing for auth apis
    api.add_resource(RegisterApi, '/api/auth/register')
    api.add_resource(LoginApi, '/api/auth/login')
