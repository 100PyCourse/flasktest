import random

from flasktest import db, bcrypt
from flask_login import UserMixin
from sqlalchemy.orm import relationship


# ----------------------- Models ----------------------- #
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(75), unique=True, nullable=False)
    username = db.Column(db.String(75), unique=False, nullable=False)
    password = db.Column(db.String(25), unique=False, nullable=False)
    reset_key = db.Column(db.String(6), unique=False, nullable=True)
    # relationships
    countries_games = db.relationship("CountriesData", backref="countries_user")
    wordle_games = db.relationship("WordleData", backref="wordle_user")
    numbers_games = db.relationship("NumbersData", backref="numbers_user")

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"


class CountriesData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))# relationship
    country1 = db.Column(db.Integer, unique=False, nullable=True)
    country2 = db.Column(db.Integer, unique=False, nullable=True)
    country_streak = db.Column(db.Integer, unique=False, nullable=True)
    country_record = db.Column(db.Integer, unique=False, nullable=True)

    def __repr__(self):
        return f"CountriesData(id={self.id}, user_id={self.user_id}, country1={self.country1}," \
               f"country2={self.country2}, country_streak={self.country_streak}," \
               f"country_record={self.country_record})"


class WordleData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))# relationship
    wordle_answer = db.Column(db.String(100), unique=False, nullable=True)
    wordle_round = db.Column(db.Integer, unique=False, nullable=True)
    wordle_guess1 = db.Column(db.String(100), unique=False, nullable=True)
    wordle_guess2 = db.Column(db.String(100), unique=False, nullable=True)
    wordle_guess3 = db.Column(db.String(100), unique=False, nullable=True)
    wordle_guess4 = db.Column(db.String(100), unique=False, nullable=True)
    wordle_guess5 = db.Column(db.String(100), unique=False, nullable=True)
    wordle_win_round = db.Column(db.Integer, unique=False, nullable=True)
    wordle_game_state = db.Column(db.String(10), unique=False, nullable=True)

    def __repr__(self):
        return f"WordleData(id={self.id}, user_id={self.user_id}," \
               f"game_state={self.wordle_game_state}, answer={self.wordle_answer})"


class NumbersData(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # relationship
    numbers_start = db.Column(db.Float(), nullable=False)
    numbers_stop = db.Column(db.Float(), nullable=True, default=-1)
    numbers_time = db.Column(db.Float(), nullable=True, default=-1)

    def __repr__(self):
        return f"NumbersData(id={self.id}, user_id={self.user_id}," \
               f" numbers_time={self.numbers_time})"


class APIData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    api_name = db.Column(db.String(30), unique=True, nullable=False)
    last_used = db.Column(db.Integer, unique=False, nullable=True)
    timer = db.Column(db.Integer, unique=False, nullable=True)


# -User------------------ Model functions ----------------------- #
def add_test_user(email, pw_hash):
    # noinspection PyArgumentList
    test_user = User(
        email=email,
        username="tester",
        password=pw_hash,
        reset_key=000000,
    )
    return test_user


def add_new_user(email, username, hashed_password, reset_key=000000):
    """
    Takes register_form input and creates a new user with default settings.
    """
    # noinspection PyArgumentList
    new_user = User(
        email=email.data,
        username=username.data,
        password=hashed_password,
        reset_key=reset_key,
    )
    db.session.add(new_user)
    db.session.commit()

    countries_data = CountriesData(
        country1=random.randint(1, 40),
        country2=random.randint(1, 40),
        country_streak=0,
        country_record=0,
        user_id=new_user.id,
    )
    db.session.add(countries_data)
    db.session.commit()


def do_passwords_match(user, password):
    if bcrypt.check_password_hash(user.password, password.data):
        return True
    return False


def change_password(user_id, hashed_password):
    user = User.query.get(user_id)
    user.password = hashed_password
    user.reset_key = None
    db.session.commit()


# -Countries------------- Model functions ----------------------- #
def add_new_countries(user_id):
    new_countries = CountriesData(
        user_id=user_id,
        country1=random.randint(1, 30),
        country2=random.randint(1, 30),
        country_streak=0,
        country_record=0,
    )
    return new_countries


# -wordle---------------- Model functions ----------------------- #
def add_new_wordle(user_id, answer):
    new_wordle = WordleData(
        user_id=user_id,
        wordle_answer=answer,
        wordle_round=0,
        wordle_game_state="busy",
    )
    return new_wordle


