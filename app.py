from flask import Flask
from models.db import initialize_db
from api import initialize_api

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
        'host': 'mongodb://localhost/book_library'
    }
initialize_db(app)
initialize_api(app)


app.run()
