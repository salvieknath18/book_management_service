from flask import request, Response
from services.analytics_service import get_genre_books
from flask_restful import Resource
from services.book_service import sort_by_genre
import json


class BooksGenre(Resource):

    def get(self):
        books_data = sort_by_genre()
        return Response(json.dumps(books_data), mimetype="application/json", status=200)

    @staticmethod
    def post():
        body = request.get_json()
        genre = body['genre']
        books = get_genre_books(genre)
        return Response(books, mimetype="application/json", status=200)
