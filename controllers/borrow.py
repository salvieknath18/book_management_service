from flask import request, Response
import datetime
from services.borrow import add_entry, update_entry, delete_entry, get_entry, get_all_entries
from services.borrow import borrow_book_copy, remove_book_copy
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError

from errors import SchemaValidationError, BookAlreadyExistsError, InternalServerError, UpdatingBookError, \
    DeletingBookError, BookNotExistsError


class BookEntries(Resource):
    @jwt_required()
    def get(self):
        books = get_all_entries()
        return Response(books, mimetype="application/json", status=200)

    @jwt_required()
    def post(self):
        try:
            body = request.get_json()
            entry_data = dict()
            entry_data['book_id'] = body['book_id']
            entry_data['isbn'] = body['isbn']
            entry_data['user_id'] = body['user_id']
            entry_data['status'] = body['status']
            entry_data['borrow_date'] = datetime.datetime.strptime(body['borrow_date'], "%d/%m/%Y  %H:%M:%S")
            entry_data['return_date'] = datetime.datetime.strptime(body['return_date'], "%d/%m/%Y  %H:%M:%S")
            obj_id = add_entry(entry_data)
            return {'success': f"Created book with id {obj_id}"}, 200
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except NotUniqueError:
            raise BookAlreadyExistsError
        except Exception:
            raise InternalServerError


class BookEntry(Resource):
    @jwt_required()
    def put(self, obj_id):
        try:
            body = request.get_json()
            entry_data = dict()
            entry_data['copy_id'] = body['copy_id']
            entry_data['isbn'] = body['isbn']
            entry_data['user_id'] = body['user_id']
            entry_data['status'] = body['status']
            entry_data['borrow_date'] = datetime.datetime.strptime(body['borrow_date'], "%d/%m/%Y  %H:%M:%S")
            entry_data['return_date'] = datetime.datetime.strptime(body['return_date'], "%d/%m/%Y  %H:%M:%S")
            updated_data = update_entry(obj_id, entry_data)
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
            delete_entry(obj_id)
            return 'success', 200
        except DoesNotExist:
            raise BookNotExistsError
        except Exception:
            raise DeletingBookError

    @jwt_required()
    def get(self, obj_id):
        try:
            book = get_entry(obj_id)
            return Response(book, mimetype="application/json", status=200)
        except DoesNotExist:
            raise BookNotExistsError
        except Exception:
            raise InternalServerError


class BorrowBookCopy(Resource):
    @staticmethod
    def get(copy_id):
        book = borrow_book_copy(copy_id)
        return Response(book, mimetype="application/json", status=200)


class ReturnBookCopy(Resource):
    @staticmethod
    def get(copy_id):
        book = remove_book_copy(copy_id)
        return Response(book, mimetype="application/json", status=200)
