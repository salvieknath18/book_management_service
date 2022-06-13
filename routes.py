from controllers.book_controller import BooksApi, BookApi
from controllers.user_controller import UsersApi, UserApi
from controllers.auth_controller import RegisterApi, LoginApi
from controllers.borrow_controller import BorrowBook, ReturnBook, BorrowEntries, AssignBookByAdmin
from controllers.analytics_controller import BooksGenre


def initialize_routes(api):
    # Routing for books apis
    api.add_resource(BooksApi, '/api/books')
    api.add_resource(BookApi, '/api/book/<id>')

    # Routing for User apis
    api.add_resource(UsersApi, '/api/users')
    api.add_resource(UserApi, '/api/user/<id>')

    # Routing for auth apis
    api.add_resource(RegisterApi, '/api/auth/register')
    api.add_resource(LoginApi, '/api/auth/login')

    # Borrow Book
    api.add_resource(BorrowBook, '/api/borrowBook')
    api.add_resource(AssignBookByAdmin, '/api/assignBook')
    api.add_resource(ReturnBook, '/api/returnBook')

    # Analytics (we can add more analytics api as per requirements
    api.add_resource(BooksGenre, '/api/analytics/booksByGenre')
    api.add_resource(BorrowEntries, '/api/analytics/borrowEntries')
