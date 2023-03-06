"""
Handles logic for the countries page.
Handles data and images.
"""

import pandas as pd
import random

from flasktest.models import CountriesData
from flasktest import db

df_europe_path = "flasktest/static/data/games/countries/df_europe.csv"


def get_country_name(number):
    """
    Takes a number(int) to compare to df_europe.
    Returns the name(str) of the country.
    """
    df_europe = pd.read_csv(df_europe_path)
    countries = df_europe.Name.tolist()
    return countries[number]


def get_country_size(number):
    """
    Takes a number(int) to compare to df_europe.
    Returns the size(int) of the country in square km.
    """
    df_europe = pd.read_csv(df_europe_path)
    sizes = df_europe.Size.tolist()
    return int(sizes[number])


def get_country_path(number):
    """
    Takes a number(int) to compare to df_europe.
    Returns the location(str) of the country's image.
    """
    df_europe = pd.read_csv(df_europe_path)
    paths = df_europe.FilePath.tolist()
    return paths[number]


def evaluate_countries_game(guess, user_id):
    """"
    Takes a users guess(str) and a user id(int).
    Compares country sizes and updates db.
    Returns countries_data.
    """
    countries_data = CountriesData.query.filter_by(user_id=user_id).first()
    size_old = int(get_country_size(countries_data.country_old))
    size_new = int(get_country_size(countries_data.country_new))

    if guess == "Larger" and size_new >= size_old:
        # User guessed correctly
        countries_data.country_streak += 1
        if countries_data.country_streak > countries_data.country_record:
            countries_data.country_record = countries_data.country_streak

    elif guess == "Smaller" and size_new <= size_old:
        # User guessed correctly
        countries_data.country_streak += 1
        if countries_data.country_streak > countries_data.country_record:
            countries_data.country_record = countries_data.country_streak

    else:
        # User guessed incorrectly
        countries_data.country_streak = 0

    countries_data.country_old = countries_data.country_new
    while countries_data.country_new == countries_data.country_old:
        countries_data.country_new = random.randint(1, 44)

    db.session.commit()

    return countries_data

