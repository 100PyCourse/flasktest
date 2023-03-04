import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap


flask_key = os.environ["flask_key"]
sqlite_uri = os.environ["sqlite_uri"]

app = Flask(__name__)
app.config["SECRET_KEY"] = flask_key
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{sqlite_uri}\\website_database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

Bootstrap(app)

from flasktest import routes
