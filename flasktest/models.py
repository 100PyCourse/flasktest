"""
Contains all models and their methods for the flask app.
"""

import random

from flasktest import db, bcrypt
from flasktest.imports.wordle_imp import Wordle
from flask_login import UserMixin
from sqlalchemy.orm import relationship


# ----------------------- Models ----------------------- #
class User(db.Model, UserMixin):
    """
    Stores the User login data and their relationships.
    """
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
    """
    Stores Users info on Countries game.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # relationship
    country_old = db.Column(db.Integer, unique=False, nullable=True)
    country_new = db.Column(db.Integer, unique=False, nullable=True)
    country_streak = db.Column(db.Integer, unique=False, nullable=True)
    country_record = db.Column(db.Integer, unique=False, nullable=True)

    def __repr__(self):
        return f"CountriesData(id={self.id}, user_id={self.user_id}, country_old={self.country_old}," \
               f"country_new={self.country_new}, country_streak={self.country_streak}," \
               f"country_record={self.country_record})"


class WordleData(db.Model):
    """
    Stores Users info on Wordle game.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # relationship
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
    """
    Stores Users info on Numbers game.
    """
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # relationship
    numbers_start = db.Column(db.Float(), nullable=False)
    numbers_stop = db.Column(db.Float(), nullable=True, default=-1)
    numbers_time = db.Column(db.Float(), nullable=True, default=-1)

    def __repr__(self):
        return f"NumbersData(id={self.id}, user_id={self.user_id}," \
               f" numbers_time={self.numbers_time})"


class APIData(db.Model):
    """
    Stores pubg api availability.
    """
    id = db.Column(db.Integer, primary_key=True)
    api_name = db.Column(db.String(30), unique=True, nullable=False)
    last_used = db.Column(db.Integer, unique=False, nullable=True)
    timer = db.Column(db.Integer, unique=False, nullable=True)


# -User------------------ Model functions ----------------------- #
def add_test_user(email, username, hashed_password, reset_key=000000):
    """
    Takes register_form input and creates a new TEST user with default settings.
    """
    # noinspection PyArgumentList
    new_user = User(
        email=email,
        username=username,
        password=hashed_password,
        reset_key=reset_key,
    )
    db.session.add(new_user)
    db.session.commit()

    countries_data = CountriesData(
        country_old=random.randint(1, 40),
        country_new=random.randint(1, 40),
        country_streak=0,
        country_record=0,
        user_id=new_user.id,
    )
    db.session.add(countries_data)
    db.session.commit()


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
    """
    Takes a user(class) and a password(str) to match in the database.
    Returns True(bool) match.
    Else returns False(bool)
    """
    if bcrypt.check_password_hash(user.password, password.data):
        return True
    return False


def change_password(user_id, hashed_password):
    """
    Takes a user_id(int) and a hashes_password(str)
    Updates the password in the database.
    """
    user = User.query.get(user_id)
    user.password = hashed_password
    user.reset_key = None
    db.session.commit()


# -Countries------------- Model functions ----------------------- #
def add_new_countries(user_id):
    """
    Takes a user_id(int).
    Returns a new_country(class) for the Countries game.
    """
    new_countries = CountriesData(
        user_id=user_id,
        country_old=random.randint(1, 30),
        country_new=random.randint(1, 30),
        country_streak=0,
        country_record=0,
    )
    return new_countries


# -wordle---------------- Model functions ----------------------- #
def add_new_wordle(user_id, answer):
    """
    Takes a user_id(int) and an answer(str).
    Returns a new_wordle(class) for the Wordle game.
    """
    new_wordle = WordleData(
        user_id=user_id,
        wordle_answer=answer,
        wordle_round=0,
        wordle_game_state="busy",
    )
    return new_wordle


def start_new_wordle(user_id):
    """
    Takes a user_id(int), creates a new Wordle game and saves it in the Users data.
    Returns a new_wordle(class) for the Wordle game.
    """
    wordle_answer = Wordle(random.choice(Wordle.word_list)).answer
    wordle_divs = Wordle(random.choice(Wordle.word_list)).game_start
    wordle_data = add_new_wordle(user_id=user_id, answer=wordle_answer)
    db.session.add(wordle_data)
    db.session.commit()
    return wordle_divs


def get_last_wordle_guess(wordle_data):
    """
    Takes a Users wordle_data(class) and returns the Users last made guess.
    """
    if wordle_data.wordle_guess4 is not None:
        return wordle_data.wordle_guess4

    if wordle_data.wordle_guess3 is not None:
        return wordle_data.wordle_guess3

    if wordle_data.wordle_guess2 is not None:
        return wordle_data.wordle_guess2

    if wordle_data.wordle_guess1 is not None:
        return wordle_data.wordle_guess1

    if wordle_data.wordle_guess1 is not None:
        return wordle_data.wordle_guess1


def play_wordle_game(wordle_guess, user_id):
    """
    Handles the logic for playing the Wordle game.
    Takes a Users wordle_guess(str) and user_id(int).
    Returns the game state(str) and the wordle_divs(list) to be rendered.
    """
    descending = WordleData.query.order_by(WordleData.id.desc())
    wordle_data = descending.filter_by(user_id=user_id).first()
    wordle_game = Wordle(wordle_data.wordle_answer)
    wordle_divs = wordle_game.game_start

    # There is an active game
    game_state = "busy"
    # Check for win
    if wordle_data.wordle_answer == wordle_guess.upper():
        wordle_data.wordle_game_state = "win"
        game_state = "win"

    if wordle_data.wordle_round == 4:
        wordle_game = Wordle(wordle_data.wordle_answer)
        wordle_divs[:5] = wordle_game.round1_data(wordle_data.wordle_guess1,
                                                  wordle_data.wordle_answer)
        wordle_divs[5:10] = wordle_game.round2_data(wordle_data.wordle_guess2,
                                                    wordle_data.wordle_answer)
        wordle_divs[10:15] = wordle_game.round3_data(wordle_data.wordle_guess3,
                                                     wordle_data.wordle_answer)
        wordle_divs[15:20] = wordle_game.round4_data(wordle_data.wordle_guess4,
                                                     wordle_data.wordle_answer)
        wordle_divs[20:25] = wordle_game.round5_data(wordle_guess.upper(),
                                                     wordle_data.wordle_answer)
        wordle_data.wordle_round = 5
        wordle_data.wordle_guess5 = wordle_guess.upper()
        if game_state == "win":
            wordle_data.wordle_win_round = 5
        else:
            game_state = "loss"
            wordle_data.wordle_game_state = "loss"
            wordle_data.wordle_win_round = -1

    elif wordle_data.wordle_round == 3:
        wordle_divs[:5] = wordle_game.round1_data(wordle_data.wordle_guess1,
                                                  wordle_data.wordle_answer)
        wordle_divs[5:10] = wordle_game.round2_data(wordle_data.wordle_guess2,
                                                    wordle_data.wordle_answer)
        wordle_divs[10:15] = wordle_game.round3_data(wordle_data.wordle_guess3,
                                                     wordle_data.wordle_answer)
        wordle_divs[15:20] = wordle_game.round4_data(wordle_guess.upper(),
                                                     wordle_data.wordle_answer)
        wordle_data.wordle_round = 4
        wordle_data.wordle_guess4 = wordle_guess.upper()
        if game_state == "win":
            wordle_data.wordle_win_round = 4

    elif wordle_data.wordle_round == 2:
        wordle_divs[:5] = wordle_game.round1_data(wordle_data.wordle_guess1,
                                                  wordle_data.wordle_answer)
        wordle_divs[5:10] = wordle_game.round2_data(wordle_data.wordle_guess2,
                                                    wordle_data.wordle_answer)
        wordle_divs[10:15] = wordle_game.round3_data(wordle_guess.upper(),
                                                     wordle_data.wordle_answer)
        wordle_data.wordle_round = 3
        wordle_data.wordle_guess3 = wordle_guess.upper()
        if game_state == "win":
            wordle_data.wordle_win_round = 3

    elif wordle_data.wordle_round == 1:
        wordle_divs[:5] = wordle_game.round1_data(wordle_data.wordle_guess1,
                                                  wordle_data.wordle_answer)
        wordle_divs[5:10] = wordle_game.round2_data(wordle_guess.upper(),
                                                    wordle_data.wordle_answer)
        wordle_data.wordle_round = 2
        wordle_data.wordle_guess2 = wordle_guess.upper()
        if game_state == "win":
            wordle_data.wordle_win_round = 2

    if wordle_data.wordle_round == 0:
        # Response after 1st guess
        wordle_divs[:5] = wordle_game.round1_data(wordle_guess.upper(),
                                                  wordle_data.wordle_answer)
        wordle_data.wordle_round = 1
        wordle_data.wordle_guess1 = wordle_guess.upper()
        if game_state == "win":
            wordle_data.wordle_win_round = 1

    db.session.commit()
    return game_state, wordle_divs
