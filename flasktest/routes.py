import random
import math
import smtplib
import time
import os

from flask import render_template, redirect, url_for, request, flash, session
from flask_login import login_user, LoginManager, login_required, logout_user

import flasktest.models
from flasktest import db, app, bcrypt
from flasktest.models import User, CountriesData, WordleData, NumbersData, APIData, add_test_user,\
    add_new_user, start_new_wordle, play_wordle_game, get_last_wordle_guess
from flasktest.imports.forms_imp import RegisterForm, LoginForm, EmailForm, ResetForm,\
    SearchPUBGForm, CountryForm, WordleForm, NumbersForm
from flasktest.imports.pubg_imp import get_player_id, get_seasons, get_all_season_stats,\
    create_dataframe, create_kills_bar, create_damage_bar, create_distance_bar
from flasktest.imports.countries_imp import get_country_name, get_country_size, get_country_path,\
    evaluate_countries_game
from flasktest.imports.numbers_imp import create_numbers_divs


GMAIL_EMAIL = os.environ["GMAIL_EMAIL"]
GMAIL_PASS = os.environ["GMAIL_PASS"]
GMAIL_SMTP = os.environ["GMAIL_SMTP"]
TEST_EMAIL = os.environ["TEST_EMAIL"]
TEST_EMAIL2 = os.environ["TEST_EMAIL2"]

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(str(user_id))


# ----------------------- Base routes ----------------------- #
@app.route("/")
def index():
    return redirect("login")


@app.route("/fresh")
def base():
    """Create two dummy accounts and API defaults after db reset"""
    hashed_password = bcrypt.generate_password_hash("test1234")
    add_test_user(email=TEST_EMAIL, username="test1", hashed_password=hashed_password)
    add_test_user(email=TEST_EMAIL2, username="test2", hashed_password=hashed_password)
    pubg_api = APIData(api_name="pubg", last_used=math.floor(time.time()), timer=60)
    db.session.add(pubg_api)
    db.session.commit()
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    register_form = RegisterForm()

    if request.method == "GET":
        return render_template("/landing/login.html",
                               login_form=login_form,
                               register_form=register_form)

    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()

        if not flasktest.models.do_passwords_match(user, login_form.password):
            flash("Password incorrect.")

        else:
            # Login successful
            login_user(user, remember=True)
            session["id"] = user.id
            return redirect(url_for("home"))

    # Unsuccessful attempts
    return render_template("/landing/login.html",
                           login_form=login_form,
                           register_form=register_form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    register_form = RegisterForm()

    if request.method == "GET":
        return render_template("/landing/register.html",
                               register_form=register_form)

    if register_form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(register_form.password.data)
        add_new_user(
            email=register_form.email,
            username=register_form.username,
            hashed_password=hashed_password,
            )
        return redirect(url_for("login"))

    # Form not validated
    return render_template("/landing/register.html",
                           register_form=register_form)


@app.route("/request-reset", methods=["GET", "POST"])
def request_reset():
    email_form = EmailForm()

    if request.method == "GET":
        return render_template("/landing/request_reset.html",
                               email_form=email_form)

    # Request reset attempt
    if email_form.validate_on_submit():
        user = User.query.filter_by(email=email_form.email.data).first()

        reset_code = random.randint(100000, 999999)
        user.reset_key = reset_code
        db.session.commit()
        with smtplib.SMTP(GMAIL_SMTP) as connection:
            connection.starttls()
            connection.login(user=GMAIL_EMAIL, password=GMAIL_PASS)
            connection.sendmail(
                from_addr=GMAIL_EMAIL,
                to_addrs=user.email,
                msg=f"Subject:Reset Code\n\nYour reset code: {reset_code}"
            )
            flash("Code hes been send!")
            return redirect(url_for("enter_reset"))

    # Request reset form not validated
    return render_template("/landing/request_reset.html",
                           email_form=email_form)


@app.route("/enter-reset", methods=["GET", "POST"])
def enter_reset():
    reset_form = ResetForm()

    if request.method == "GET":
        return render_template("/landing/enter_reset.html",
                               reset_form=reset_form)

    # Reset attempt
    if reset_form.validate_on_submit():
        user = User.query.filter_by(email=reset_form.email.data).first()

        # User did not request a reset
        if user.reset_key == 000000 or None:
            flash("Unauthorised request!")
            return render_template("/landing/enter_reset.html",
                                   reset_form=reset_form)

        # Incorrect reset code
        if not user.reset_key == reset_form.reset_code.data:
            flash("Incorrect email or code!")
            return render_template("/landing/enter_reset.html",
                                   reset_form=reset_form)

        # Password reset successful
        hashed_password = bcrypt.generate_password_hash(reset_form.password.data)
        flasktest.models.change_password(user.id, hashed_password)
        return redirect("login")

    # Enter reset form not validated
    return render_template("/landing/enter_reset.html",
                           reset_form=reset_form)


# ----------------------- HOME route ----------------------- #
@app.route("/home")
@login_required
def home():
    return render_template("home.html",
                           page="home")


# ----------------------- API routes ----------------------- #
@app.route("/api/pubg", methods=["POST", "GET"])
@login_required
def pubg():
    pubg_form = SearchPUBGForm()
    kills_img = "../static/images/api/pubg/example_kills.png"
    damage_img = "../static/images/api/pubg/example_damage.png"
    distance_img = "../static/images/api/pubg/example_distance.png"
    df_path = "flasktest/static/data/api/pubg/df_"
    pubg_data = APIData.query.filter_by(api_name="pubg").first()

    if request.method == "GET":
        return render_template("/api/pubg.html", pubg_form=pubg_form, kills_img=kills_img,
                               damage_img=damage_img, distance_img=distance_img, page="pubg")

    if pubg_form.validate_on_submit():
        name = pubg_form.name.data
        game_mode = pubg_form.game_mode.data + pubg_form.perspective.data
        save_mode = game_mode.replace("-", "_")

        # Check for existing data before contacting API
        if os.path.exists(f"{df_path}{name}_{save_mode}.csv"):
            kills_img, damage_img, distance_img = \
                flasktest.imports.pubg_imp.load_old_pubg_data(df_path, name, game_mode, save_mode)

            return render_template("/api/pubg.html", pubg_form=pubg_form, kills_img=kills_img,
                                   damage_img=damage_img, distance_img=distance_img,
                                   scrollToAnchor="pubg-section", page="pubg")

        # No data found - contact API
        # Check API availability
        if (pubg_data.last_used + 60) > time.time():
            # API used in last 60 seconds
            flash_message = flasktest.imports.pubg_imp.get_pubg_cooldown_message()
            flash(flash_message)
            return render_template("/api/pubg.html", pubg_form=pubg_form, kills_img=kills_img,
                                   damage_img=damage_img, distance_img=distance_img,
                                   scrollToAnchor="pubg-section", page="pubg")

        id_code, id_response = get_player_id(name)
        if not id_code == 200:
            # Unsuccessful request - see pubg_imp.py for more info
            if id_code == 429:
                # Request limit reached
                flasktest.imports.pubg_imp.update_pubg_api_data()

            flash_message = id_response
            flash(flash_message)
            return render_template("/api/pubg.html", pubg_form=pubg_form, kills_img=kills_img,
                                   damage_img=damage_img, distance_img=distance_img,
                                   scrollToAnchor="pubg-section", page="pubg")

        player_id = id_response
        # Player ID retrieved successfully
        seasons_code, seasons_response = get_seasons()
        if not seasons_code == 200:
            # Unsuccessful request - see pubg_imp.py for more info
            flash_message = seasons_response
            if seasons_code == 429:
                # Request limit reached
                flasktest.imports.pubg_imp.update_pubg_api_data()

            flash(flash_message)
            return render_template("/api/pubg.html", pubg_form=pubg_form, kills_img=kills_img,
                                   damage_img=damage_img, distance_img=distance_img,
                                   scrollToAnchor="pubg-section", page="pubg")

        valid_seasons = seasons_response
        # Valid seasons retrieved successfully
        stats_code, stats_response = get_all_season_stats(player_id, valid_seasons, game_mode)
        if not stats_code == 200:
            # Unsuccessful request - see pubg_imp.py for more info
            flash_message = stats_response
            if stats_code == 429:
                # Request limit reached
                flasktest.imports.pubg_imp.update_pubg_api_data()

            flash(flash_message)
            return render_template("/api/pubg.html", pubg_form=pubg_form, kills_img=kills_img,
                                   damage_img=damage_img, distance_img=distance_img,
                                   scrollToAnchor="pubg-section", page="pubg")

        player_stats = stats_response
        # Player stats retrieved successfully
        if len(player_stats[0]) < 2:
            # Check if player was active in at least 2 seasons, else draw no graph
            flash("Player has insufficient stats to generate graph")
            return render_template("/api/pubg.html", pubg_form=pubg_form, kills_img=kills_img,
                                   damage_img=damage_img, distance_img=distance_img,
                                   scrollToAnchor="pubg-section", page="pubg")

        # Success
        new_df = create_dataframe(player_stats, name, save_mode)
        kills_img = create_kills_bar(new_df, name, game_mode)
        damage_img = create_damage_bar(new_df, name, game_mode)
        distance_img = create_distance_bar(new_df, name, game_mode)
        # Update api db with timestamp
        flasktest.imports.pubg_imp.update_pubg_api_data()
        return render_template("/api/pubg.html", pubg_form=pubg_form, kills_img=kills_img,
                               damage_img=damage_img, distance_img=distance_img,
                               scrollToAnchor="pubg-section", page="pubg")

    # Form not validated
    return render_template("/api/pubg.html", pubg_form=pubg_form, kills_img=kills_img,
                           damage_img=damage_img, distance_img=distance_img,
                           scrollToAnchor="pubg-section", page="pubg")


# ----------------------- Game routes ----------------------- #
@app.route("/games/countries", methods=["GET", "POST"])
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


@app.route("/games/wordle", methods=["POST", "GET"])
@login_required
def wordle():
    return render_template("games/wordle.html", page="wordle")


@app.route("/games/play-wordle", methods=["POST", "GET"])
@login_required
def play_wordle():
    wordle_form = WordleForm()
    # Get the users last played game
    descending = WordleData.query.order_by(WordleData.id.desc())
    wordle_data = descending.filter_by(user_id=session["id"]).first()

    print(wordle_data.wordle_guess4)

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


@app.route("/games/numbers", methods=["POST", "GET"])
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
