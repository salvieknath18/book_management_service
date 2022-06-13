from flask import request, Response, jsonify
import datetime
from services.book_service import add_book, update_book, delete_book, get_book, get_all_books, \
    clean_all_books, clean_book
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from errors import SchemaValidationError, BookAlreadyExistsError, InternalServerError, UpdatingBookError, \
    DeletingBookError, BookNotExistsError
from services.user_service import roles_required
import json


class BooksApi(Resource):

    @staticmethod
    def get():
        books = get_all_books()
        books_data = clean_all_books(books)
        return Response(json.dumps(books_data), mimetype="application/json", status=200)

    @jwt_required()
    @roles_required('admin', 'editor')
    def post(self):
        try:
            body = request.get_json()
            book_data = dict()
            book_data['isbn'] = body['isbn']
            book_data['title'] = body['title']
            book_data['description'] = body['description']
            book_data['genre'] = body['genre']
            book_data['author'] = body['author']
            book_data['total_count'] = body['total_count']
            book_data['available_count'] = body['available_count']
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
    @roles_required('admin', 'editor')
    def put(self, obj_id):
        try:
            body = request.get_json()
            book_data = dict()
            book_data['isbn'] = body['isbn']
            book_data['title'] = body['title']
            book_data['description'] = body['description']
            book_data['genre'] = body['genre']
            book_data['author'] = body['author']
            book_data['total_count'] = body['total_count']
            book_data['available_count'] = body['available_count']
            book_data['year_published'] = datetime.datetime.strptime(body['year_published'], "%d/%m/%Y  %H:%M:%S")
            updated_book = update_book(obj_id, book_data)
            updated_data = clean_book(updated_book)
            return Response(json.dumps(updated_data), mimetype="application/json", status=200)
        except InvalidQueryError:
            raise SchemaValidationError
        except DoesNotExist:
            raise UpdatingBookError
        except Exception:
            raise InternalServerError

    @jwt_required()
    @roles_required('admin', 'editor')
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
            book = clean_book(get_book(obj_id))
            return Response(json.dumps(book), mimetype="application/json", status=200)
        except DoesNotExist:
            raise BookNotExistsError
        except Exception:
            raise InternalServerError

# Future Scope : If we have to track copies of book we can implement following APIs with few modifications in model
# class AddBookCopy(Resource):
#     @staticmethod
#     def post(obj_id):
#         book = add_book_copy(obj_id)
#         return Response(book, mimetype="application/json", status=200)
#
#
# class RemoveBookCopy(Resource):
#     @staticmethod
#     def delete(obj_id, copy_id):
#         book = remove_book_copy(obj_id, copy_id)
#         return Response(book, mimetype="application/json", status=200)
