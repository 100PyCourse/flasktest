import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt

FLASK_KEY = os.environ["FLASK_KEY"]
SQLITE_URI = os.environ["SQLITE_URI"]
WEBSITE_DB_URI = os.environ["WEBSITE_DB_URI"]

app = Flask(__name__)
app.config["SECRET_KEY"] = FLASK_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{SQLITE_URI}\\website_database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
Bootstrap(app)

from flasktest import routes

with app.app_context():
    if not os.path.exists(f"{WEBSITE_DB_URI}\\website_database.db"):
        db.create_all()
