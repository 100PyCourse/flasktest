"""
Handles logic for the countries page.
Handles data and images.
"""

import pandas as pd


def get_country_name(number):
    """
    Takes a number(int) to compare to df_europe.
    Returns the name(str) of the country.
    """
    df_europe = pd.read_csv("flasktest/static/data/games/countries/df_europe.csv")
    countries = df_europe.Name.tolist()
    return countries[number]


def get_country_size(number):
    """
    Takes a number(int) to compare to df_europe.
    Returns the size(int) of the country in square km.
    """
    df_europe = pd.read_csv("flasktest/static/data/games/countries/df_europe.csv")
    sizes = df_europe.Size.tolist()
    return int(sizes[number])


def get_country_path(number):
    """
    Takes a number(int) to compare to df_europe.
    Returns the location(str) of the country's image.
    """
    df_europe = pd.read_csv("flasktest/static/data/games/countries/df_europe.csv")
    paths = df_europe.FilePath.tolist()
    return paths[number]
