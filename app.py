from flask import Flask
from models.db import initialize_db
from api import initialize_api

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
        'host': 'mongodb://localhost/book_library_1'
    }

initialize_api(app)
initialize_db(app)


if __name__ == "__main__":
    app.run()
