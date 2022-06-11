from flask import request, Response
from services.borrow_service import delete_entry, get_entry, get_all_entries
from services.borrow_service import borrow_book_copy, remove_book_copy
from services.user_service import get_current_user, get_user
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from mongoengine.errors import DoesNotExist

from errors import InternalServerError, DeletingBookError, BookNotExistsError


class BorrowEntries(Resource):
    @jwt_required()
    def get(self):
        books = get_all_entries()
        return Response(books, mimetype="application/json", status=200)


class BookEntry(Resource):
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


class BorrowBook(Resource):

    @jwt_required()
    def post(self):
        body = request.get_json()
        isbn = body['isbn']
        user = get_current_user
        borrow_entry = borrow_book_copy(isbn, user)
        return Response(borrow_entry, mimetype="application/json", status=200)


class AssignBookByAdmin(Resource):

    @jwt_required()
    def post(self):
        body = request.get_json()
        isbn = body['isbn']
        user = get_user(body['member_id'])
        borrow_entry = borrow_book_copy(isbn, user)
        return Response(borrow_entry, mimetype="application/json", status=200)


class ReturnBook(Resource):

    @jwt_required()
    def post(self):
        body = request.get_json()
        isbn = body['isbn']
        user = get_current_user()
        borrow_entry = remove_book_copy(isbn, user)
        return Response(borrow_entry, mimetype="application/json", status=200)


class CollectBookByAdmin(Resource):

    @jwt_required()
    def post(self):
        body = request.get_json()
        isbn = body['isbn']
        user = get_user(body['member_id'])
        borrow_entry = remove_book_copy(isbn, user)
        return Response(borrow_entry, mimetype="application/json", status=200)
