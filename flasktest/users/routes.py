from flask import Blueprint

import random
import math
import smtplib
import time
import os

from flask import render_template, redirect, url_for, request, flash, session
from flask_login import login_user, login_required, logout_user

import flasktest.models
from flasktest import db, bcrypt
from flasktest.models import User, APIData, add_test_user, add_new_user
from flasktest.users.forms import RegisterForm, LoginForm, EmailForm, ResetForm

users = Blueprint("users", __name__)

GMAIL_EMAIL = os.environ["GMAIL_EMAIL"]
GMAIL_PASS = os.environ["GMAIL_PASS"]
GMAIL_SMTP = os.environ["GMAIL_SMTP"]
TEST_EMAIL = os.environ["TEST_EMAIL"]
TEST_EMAIL2 = os.environ["TEST_EMAIL2"]


@users.route("/")
def index():
    return redirect("login")


@users.route("/fresh")
def base():
    """Create two dummy accounts and API defaults after db reset"""
    hashed_password = bcrypt.generate_password_hash("test1234")
    add_test_user(email=TEST_EMAIL, username="test1", hashed_password=hashed_password)
    add_test_user(email=TEST_EMAIL2, username="test2", hashed_password=hashed_password)
    pubg_api = APIData(api_name="pubg", last_used=math.floor(time.time()), timer=60)
    db.session.add(pubg_api)
    db.session.commit()
    return redirect(url_for("users.login"))


@users.route("/login", methods=["GET", "POST"])
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
            return redirect(url_for("main.home"))

    # Unsuccessful attempts
    return render_template("/landing/login.html",
                           login_form=login_form,
                           register_form=register_form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("users.login"))


@users.route("/register", methods=["GET", "POST"])
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
        return redirect(url_for("users.login"))

    # Form not validated
    return render_template("/landing/register.html",
                           register_form=register_form)


@users.route("/request-reset", methods=["GET", "POST"])
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
            return redirect(url_for("users.enter_reset"))

    # Request reset form not validated
    return render_template("/landing/request_reset.html",
                           email_form=email_form)


@users.route("/enter-reset", methods=["GET", "POST"])
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