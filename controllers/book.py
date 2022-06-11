from flask import request, Response
import datetime
from services.book import add_book, update_book, delete_book, get_book, get_all_books
from services.book import add_book_copy, remove_book_copy
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError

from errors import SchemaValidationError, BookAlreadyExistsError, InternalServerError, UpdatingBookError, \
    DeletingBookError, BookNotExistsError


class BooksApi(Resource):
    @staticmethod
    def get():
        books = get_all_books()
        return Response(books, mimetype="application/json", status=200)

    @jwt_required()
    def post(self):
        try:
            body = request.get_json()
            book_data = dict()
            book_data['isbn'] = body['isbn']
            book_data['title'] = body['title']
            book_data['description'] = body['description']
            book_data['genre'] = body['genre']
            book_data['author'] = body['author']
            # To-DO copies entry
            book_data['available_copies'] = body['available_copies']
            book_data['unavailable_copies'] = body['unavailable_copies']
            book_data['year_published'] = datetime.datetime.strptime(body['year_published'], "%d/%m/%Y  %H:%M:%S")
            obj_id = add_book(book_data)
            return {'success': f"Created book with id {obj_id}"}, 200
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except NotUniqueError:
            raise BookAlreadyExistsError
        except Exception:
            raise InternalServerError


class BookApi(Resource):
    @jwt_required()
    def put(self, obj_id):
        try:
            body = request.get_json()
            book_data = dict()
            book_data['isbn'] = body['isbn']
            book_data['title'] = body['title']
            book_data['description'] = body['description']
            book_data['genre'] = body['genre']
            book_data['author'] = body['author']
            book_data['available_copies'] = body['available_copies']
            book_data['unavailable_copies'] = body['unavailable_copies']
            book_data['year_published'] = datetime.datetime.strptime(body['year_published'], "%d/%m/%Y  %H:%M:%S")
            updated_data = update_book(obj_id, book_data)
            return updated_data, 200
        except InvalidQueryError:
            raise SchemaValidationError
        except DoesNotExist:
            raise UpdatingBookError
        except Exception:
            raise InternalServerError

    @jwt_required()
    def delete(self, obj_id):
        try:
            delete_book(obj_id)
            return 'success', 200
        except DoesNotExist:
            raise BookNotExistsError
        except Exception:
            raise DeletingBookError

    @staticmethod
    def get(obj_id):
        try:
            book = get_book(obj_id)
            return Response(book, mimetype="application/json", status=200)
        except DoesNotExist:
            raise BookNotExistsError
        except Exception:
            raise InternalServerError


class AddBookCopy(Resource):
    @staticmethod
    def post(obj_id):
        book = add_book_copy(obj_id)
        return Response(book, mimetype="application/json", status=200)


class RemoveBookCopy(Resource):
    @staticmethod
    def delete(obj_id, copy_id):
        book = remove_book_copy(obj_id, copy_id)
        return Response(book, mimetype="application/json", status=200)
