from flask import request, Response
from services.borrow_service import delete_entry, get_entry, get_all_entries, clean_all_entries, clean_borrow_entry
from services.borrow_service import borrow_book_copy, remove_book_copy
from services.user_service import get_current_user, get_user
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from mongoengine.errors import DoesNotExist
from services.user_service import roles_required
from errors import InternalServerError, DeletingBookError, BookNotExistsError
import json


class BorrowEntries(Resource):
    @jwt_required()
    @roles_required('admin', 'editor')
    def get(self):
        entries = get_all_entries()
        entries_data = clean_all_entries(entries)
        return Response(json.dumps(entries_data), mimetype="application/json", status=200)


class BookEntry(Resource):
    @jwt_required()
    @roles_required('admin', 'editor')
    def delete(self, obj_id):
        try:
            delete_entry(obj_id)
            return Response('success', mimetype="application/json", status=200)
        except DoesNotExist:
            raise BookNotExistsError
        except Exception:
            raise DeletingBookError

    @jwt_required()
    @roles_required('admin', 'editor')
    def get(self, obj_id):
        try:
            book = clean_borrow_entry(get_entry(obj_id))
            return Response(json.dumps(book), mimetype="application/json", status=200)
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
        borrow_entry = clean_borrow_entry(borrow_book_copy(isbn, user))
        return Response(json.dumps(borrow_entry), mimetype="application/json", status=200)


class AssignBookByAdmin(Resource):

    @jwt_required()
    @roles_required('admin', 'editor')
    def post(self):
        body = request.get_json()
        isbn = body['isbn']
        user = get_user(body['member_id'])
        borrow_entry = clean_borrow_entry(borrow_book_copy(isbn, user))
        return Response(json.dumps(borrow_entry), mimetype="application/json", status=200)


class ReturnBook(Resource):

    @jwt_required()
    def post(self):
        body = request.get_json()
        isbn = body['isbn']
        user = get_current_user()
        borrow_entry = clean_borrow_entry(remove_book_copy(isbn, user))
        return Response(json.dumps(borrow_entry), mimetype="application/json", status=200)


class CollectBookByAdmin(Resource):

    @jwt_required()
    @roles_required('admin', 'editor')
    def post(self):
        body = request.get_json()
        isbn = body['isbn']
        user = get_user(body['member_id'])
        borrow_entry = clean_borrow_entry(remove_book_copy(isbn, user))
        return Response(json.dumps(borrow_entry), mimetype="application/json", status=200)
