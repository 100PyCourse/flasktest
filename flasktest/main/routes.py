import random
import math
import smtplib
import time
import os

from flask import render_template
from flask_login import login_required

from flask import Blueprint

main = Blueprint("main", __name__)


@main.route("/home")
@login_required
def home():
    return render_template("home.html",
                           page="home")
