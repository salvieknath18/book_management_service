from flask import request, Response
from services.analytics_service import get_genre_books
from flask_restful import Resource


class BooksGenre(Resource):

    @staticmethod
    def post():
        body = request.get_json()
        genre = body['genre']
        books = get_genre_books(genre)
        return Response(books, mimetype="application/json", status=200)
