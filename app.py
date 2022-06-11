from flask import Flask
from db import initialize_db
from api import initialize_api

app = Flask(__name__)

initialize_api(app)
initialize_db(app)


if __name__ == "__main__":
    app.run()
