from models.db import db


class Book(db.Document):
    book_id = db.StringField(required=True, unique=True)
    title_id = db.StringField(required=True)
    description = db.StringField(required=True)
    genre = db.StringField(required=True)
    author = db.StringField(required=True)
    year_published = db.DateTimeField(required=True)
    availability = db.BooleanField(required=True)
    borrower = db.ReferenceField('User')
