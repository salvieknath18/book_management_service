from db import db


class Borrow(db.Document):
    book = db.ReferenceField('Book', required=True)
    user = db.ReferenceField('User')
    borrow_date = db.DateTimeField()
    return_date = db.DateTimeField()
    status = db.StringField()

# TO-DO
# if a user is deleted then the book created by the user is also deleted. ? does it make sense
# Borrow.register_delete_rule(Book, 'isbn', db.CASCADE) #think on usecase and requirements
