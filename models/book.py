from db import db
from models.borrow import Borrow


class Book(db.Document):
    isbn = db.StringField(required=True, unique=True)
    title = db.StringField(required=True)
    description = db.StringField(required=True)
    genre = db.StringField(required=True)
    author = db.StringField(required=True)
    year_published = db.DateTimeField(required=True)
    available_copies = db.ListField(db.ReferenceField('Borrow', reverse_delete_rule=db.PULL))
    unavailable_copies = db.ListField(db.ReferenceField('Borrow', reverse_delete_rule=db.PULL))


Book.register_delete_rule(Borrow, "available_copies", db.PULL)
Book.register_delete_rule(Borrow, "unavailable_copies", db.PULL)
