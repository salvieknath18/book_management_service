from models.db import db
from flask_bcrypt import generate_password_hash, check_password_hash


class User(db.Document):
    user_id = db.StringField(required=True, unique=True)
    name = db.StringField(required=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6)
    role = db.StringField(required=True)

    # book should be pulled from the user document if the book is deleted.
    books = db.ListField(db.ReferenceField('Book', reverse_delete_rule=db.PULL))

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)
