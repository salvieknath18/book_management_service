from db import db


class Book(db.Document):

    isbn = db.StringField(required=True, unique=True)
    title = db.StringField(required=True)
    description = db.StringField(required=True)
    genre = db.StringField(required=True)
    author = db.StringField(required=True)
    year_published = db.DateTimeField(required=True)
    total_count = db.IntField(required=True)
    available_count = db.IntField(required=True)
