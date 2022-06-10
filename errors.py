class InternalServerError(Exception):
    pass


class SchemaValidationError(Exception):
    pass


class BookAlreadyExistsError(Exception):
    pass


class UpdatingBookError(Exception):
    pass


class DeletingBookError(Exception):
    pass


class BookNotExistsError(Exception):
    pass


class EmailAlreadyExistsError(Exception):
    pass


class UnauthorizedError(Exception):
    pass


class EmailDoesnotExistsError(Exception):
    pass


class BadTokenError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class UpdatingUserError(Exception):
    pass


class DeletingUserError(Exception):
    pass


class UserNotExistsError(Exception):
    pass




errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },
     "SchemaValidationError": {
         "message": "Request is missing required fields",
         "status": 400
     },
     "BookAlreadyExistsError": {
         "message": "Book with given name already exists",
         "status": 400
     },
     "UpdatingBookError": {
         "message": "Updating book added by other is forbidden",
         "status": 403
     },
     "DeletingBookError": {
         "message": "Deleting book added by other is forbidden",
         "status": 403
     },
     "BookNotExistsError": {
         "message": "Book with given id doesn't exists",
         "status": 400
     },
     "EmailAlreadyExistsError": {
         "message": "User with given email address already exists",
         "status": 400
     },
     "UnauthorizedError": {
         "message": "Invalid username or password",
         "status": 401
    },
    "EmailDoesnotExistsError": {
        "message": "Couldn't find the user with given email address",
        "status": 400
    },
    "BadTokenError": {
        "message": "Invalid token",
        "status": 403
    },
    "UserAlreadyExistsError": {
         "message": "User with given name already exists",
         "status": 400
     },
    "UpdatingUserError": {
         "message": "Updating User added by other is forbidden",
         "status": 403
     },
     "DeletingUserError": {
         "message": "Deleting User added by other is forbidden",
         "status": 403
     },
     "UserNotExistsError": {
         "message": "User with given id doesn't exists",
         "status": 400
     }
}