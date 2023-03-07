import time

from flask import render_template, request, session
from flask_login import login_required

from flasktest import db
from flasktest.models import CountriesData, WordleData, NumbersData, start_new_wordle,\
    play_wordle_game, get_last_wordle_guess
from flasktest.games.forms import CountryForm, WordleForm, NumbersForm
from flasktest.games.utils import get_country_name, get_country_size, get_country_path,\
    evaluate_countries_game, create_numbers_divs

from flask import Blueprint

games = Blueprint("games", __name__)


@games.route("/games/countries", methods=["GET", "POST"])
@login_required
def countries():
    country_form = CountryForm()
    countries_data = CountriesData.query.filter_by(user_id=session["id"]).first()

    if request.method == "GET":
        return render_template("/games/countries.html",
                               country_form=country_form,
                               name1=get_country_name(countries_data.country_old),
                               size1=get_country_size(countries_data.country_old),
                               path1=get_country_path(countries_data.country_old),
                               name2=get_country_name(countries_data.country_new),
                               size2=get_country_size(countries_data.country_new),
                               path2=get_country_path(countries_data.country_new),
                               country_streak=countries_data.country_streak,
                               page="countries",
                               country_record=countries_data.country_record)

    if country_form.validate_on_submit():
        guess = country_form.select.data
        countries_data = evaluate_countries_game(guess=guess, user_id=session["id"])

        return render_template("/games/countries.html",
                               country_form=country_form,
                               name1=get_country_name(countries_data.country_old),
                               size1=get_country_size(countries_data.country_old),
                               path1=get_country_path(countries_data.country_old),
                               name2=get_country_name(countries_data.country_new),
                               size2=get_country_size(countries_data.country_new),
                               path2=get_country_path(countries_data.country_new),
                               country_streak=countries_data.country_streak,
                               country_record=countries_data.country_record,
                               page="countries",
                               scrollToAnchor="country-location")


@games.route("/games/wordle", methods=["POST", "GET"])
@login_required
def wordle():
    return render_template("games/wordle.html", page="wordle")


@games.route("/games/play-wordle", methods=["POST", "GET"])
@login_required
def play_wordle():
    wordle_form = WordleForm()
    # Get the users last played game
    descending = WordleData.query.order_by(WordleData.id.desc())
    wordle_data = descending.filter_by(user_id=session["id"]).first()

    # No games played yet
    if not wordle_data:
        # Start new game
        wordle_divs = start_new_wordle(session["id"])
        return render_template("games/play_wordle.html",
                               wordle_form=wordle_form,
                               wordle_divs=wordle_divs,
                               page="play_wordle")

    # Last game finished
    if wordle_data.wordle_game_state in ("win", "loss"):
        # Start new game
        wordle_divs = start_new_wordle(session["id"])
        return render_template("games/play_wordle.html",
                               wordle_form=wordle_form,
                               wordle_divs=wordle_divs,
                               page="play_wordle")

    # There is an active game
    if wordle_form.validate_on_submit():
        # Call play game function
        game_state, wordle_divs = play_wordle_game(wordle_guess=wordle_form.guess.data,
                                                   user_id=session["id"])

        return render_template("games/play_wordle.html",
                               wordle_form=wordle_form,
                               wordle_divs=wordle_divs,
                               game_state=game_state,
                               page="play_wordle")

    # GET request
    # Need last guessed word to recreate game state
    last_wordle_guess = get_last_wordle_guess(wordle_data=wordle_data)
    game_state, wordle_divs = play_wordle_game(wordle_guess=last_wordle_guess,
                                               user_id=session["id"])

    return render_template("games/play_wordle.html",
                           wordle_form=wordle_form,
                           wordle_divs=wordle_divs,
                           game_state=game_state,
                           page="play_wordle")


@games.route("/games/numbers", methods=["POST", "GET"])
@login_required
def numbers():
    numbers_form = NumbersForm()
    numbers_divs = create_numbers_divs()

    # Get users last unfinished game
    numbers_data = db.session.query(NumbersData)\
        .order_by(NumbersData.id.desc())\
        .filter(NumbersData.user_id == session["id"])\
        .first()
    # Get best times global
    numbers_highscores_all = db.session.query(NumbersData)\
        .order_by(NumbersData.numbers_time)\
        .filter(NumbersData.numbers_time > 0).limit(8)\
        .all()
    # Get best times personal
    numbers_highscores_self = db.session.query(NumbersData)\
        .order_by(NumbersData.numbers_time)\
        .filter(NumbersData.numbers_time > 0, NumbersData.user_id == session["id"]).limit(8)\
        .all()

    # Never played before
    if numbers_data is None:
        new_numbers = NumbersData(
            user_id=session["id"],
            numbers_start=time.time(),
        )
        db.session.add(new_numbers)
        db.session.commit()
        return render_template("/games/numbers.html",
                               numbers_form=numbers_form,
                               numbers_divs=numbers_divs,
                               numbers_highscores_self=numbers_highscores_self,
                               numbers_highscores_all=numbers_highscores_all,
                               page="numbers",
                               )

    # Played before and last game is over
    if numbers_data.numbers_time != -1:
        new_numbers = NumbersData(
            user_id=session["id"],
            numbers_start=time.time(),
        )
        db.session.add(new_numbers)
        db.session.commit()
        return render_template("/games/numbers.html",
                               numbers_form=numbers_form,
                               numbers_divs=numbers_divs,
                               numbers_highscores_self=numbers_highscores_self,
                               numbers_highscores_all=numbers_highscores_all,
                               page="numbers",
                               )

    # Game is going on pressed stop
    if numbers_form.validate_on_submit():
        numbers_data.numbers_stop = time.time()
        numbers_data.numbers_time = round((numbers_data.numbers_stop - numbers_data.numbers_start),
                                          4)
        db.session.commit()
        return render_template("/games/numbers.html",
                               numbers_form=numbers_form,
                               numbers_divs=numbers_divs,
                               numbers_highscores_self=numbers_highscores_self,
                               numbers_highscores_all=numbers_highscores_all,
                               page="numbers",
                               )

    # Game is going on and restarted
    if numbers_data.numbers_stop == -1:
        db.session.delete(numbers_data)
        db.session.commit()
        new_numbers = NumbersData(
            user_id=session["id"],
            numbers_start=time.time(),
        )
        db.session.add(new_numbers)
        db.session.commit()
        return render_template("/games/numbers.html",
                               numbers_form=numbers_form,
                               numbers_divs=numbers_divs,
                               numbers_highscores_self=numbers_highscores_self,
                               numbers_highscores_all=numbers_highscores_all,
                               page="numbers",
                               )
