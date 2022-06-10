from flask import request, Response
import datetime
from models.book import Book
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError

from errors import SchemaValidationError, BookAlreadyExistsError, InternalServerError, UpdatingBookError, \
    DeletingBookError, BookNotExistsError


class BooksApi(Resource):

    @staticmethod
    def get():
        books = Book.objects().to_json()
        return Response(books, mimetype="application/json", status=200)

    @jwt_required()
    def post(self):
        try:
            body = request.get_json()
            body['year_published'] = datetime.datetime.strptime(body['year_published'], "%d/%m/%Y  %H:%M:%S")
            book = Book(**body)
            book.save()
            book_id = book.id
            return {'book_id': str(book_id)}, 200
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except NotUniqueError:
            raise BookAlreadyExistsError
        except Exception:
            raise InternalServerError


class BookApi(Resource):
    @jwt_required()
    def put(self, book_id):
        try:
            body = request.get_json()
            Book.objects.get(book_id=book_id).update(**body)
            return '', 200
        except InvalidQueryError:
            raise SchemaValidationError
        except DoesNotExist:
            raise UpdatingBookError
        except Exception:
            raise InternalServerError

    @jwt_required()
    def delete(self, book_id):
        try:
            book = Book.objects.get(book_id=book_id)
            book.delete()
            return '', 200
        except DoesNotExist:
            raise BookNotExistsError
        except Exception:
            raise DeletingBookError

    @staticmethod
    def get(book_id):
        try:
            books = Book.objects.get(book_id=book_id).to_json()
            return Response(books, mimetype="application/json", status=200)
        except DoesNotExist:
            raise BookNotExistsError
        except Exception:
            raise InternalServerError
