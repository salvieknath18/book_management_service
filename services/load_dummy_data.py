from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, ValidationError
from services.user_service import add_user
from services.book_service import add_book
from errors import SchemaValidationError, InternalServerError
import os
import json
import datetime


class LoadDummyData(Resource):

    @staticmethod
    def get():
        try:
            with open(os.path.join(os.getcwd(), "static", "dummy_data.json")) as data_file:
                dummy_data = json.load(data_file)
                for dummy_user in dummy_data['users']:
                    add_user(dummy_user)
                for dummy_book in dummy_data['books']:
                    dummy_book['year_published'] = datetime.datetime.strptime(dummy_book['year_published'], "%d/%m/%Y")
                    add_book(dummy_book)
            return {'success': f"Loaded Dummy Data"}, 200
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except NotUniqueError:
            return {'Failure': "Duplicate data"}, 400
        except Exception:
            raise InternalServerError