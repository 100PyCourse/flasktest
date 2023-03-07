import pandas as pd
import random

from flasktest import db
from flasktest.models import CountriesData

df_europe_path = "flasktest/static/data/games/countries/df_europe.csv"
wordle_words_path = "flasktest/static/data/games/wordle/5_letter_words.csv"


# ####### Countries ####### #
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


# ####### Wordle ####### #
class Wordle:
    """
    Class containing wordle game info.
    """
    df_words = pd.read_csv(wordle_words_path)
    word_list = df_words.Word.tolist()

    def __init__(self, answer):
        self.answer = answer.upper()
        self.guess1 = ""
        self.guess2 = ""
        self.guess3 = ""
        self.guess4 = ""
        self.guess5 = ""
        self.round = 0

        self.grey = "var(--grey)"
        self.yellow = "var(--yellow)"
        self.green = "var(--green)"

        self.all_info = []
        self.empty = [".", self.grey]

        self.game_start = [self.empty for x in range(25)]

    def __repr__(self):
        return f"Wordle(" \
               f"round={self.round}, answer={self.answer})"

    def start_wordle(self):
        """
        Returns an empty grid for a new game.
        """
        return self.game_start

    def round1_data(self, guess1, answer):
        """
        Takes a guess(str) and an answer(str).
        Returns the correct divs to render the wordle page.
        """
        colors = []
        for index, letter in enumerate(guess1):
            if letter == answer[index]:
                colors.append([letter, self.green])
            elif letter in answer:
                colors.append([letter, self.yellow])
            else:
                colors.append([letter, self.grey])
        self.round += 1
        self.guess1 = guess1
        return colors

    def round2_data(self, guess2, answer):
        """
        Takes a guess(str) and an answer(str).
        Returns the correct divs to render the wordle page.
        """
        colors = []
        for index, letter in enumerate(guess2):
            if letter == answer[index]:
                colors.append([letter, self.green])
            elif letter in answer:
                colors.append([letter, self.yellow])
            else:
                colors.append([letter, self.grey])
        self.round += 1
        self.guess2 = guess2
        return colors

    def round3_data(self, guess3, answer):
        """
        Takes a guess(str) and an answer(str).
        Returns the correct divs to render the wordle page.
        """
        colors = []
        for index, letter in enumerate(guess3):
            if letter == answer[index]:
                colors.append([letter, self.green])
            elif letter in answer:
                colors.append([letter, self.yellow])
            else:
                colors.append([letter, self.grey])
        self.round += 1
        self.guess3 = guess3
        return colors

    def round4_data(self, guess4, answer):
        """
        Takes a guess(str) and an answer(str).
        Returns the correct divs to render the wordle page.
        """
        colors = []
        for index, letter in enumerate(guess4):
            if letter == answer[index]:
                colors.append([letter, self.green])
            elif letter in answer:
                colors.append([letter, self.yellow])
            else:
                colors.append([letter, self.grey])
        self.round += 1
        self.guess4 = guess4
        return colors

    def round5_data(self, guess5, answer):
        """
        Takes a guess(str) and an answer(str).
        Returns the correct divs to render the wordle page.
        """
        colors = []
        for index, letter in enumerate(guess5):
            if letter == answer[index]:
                colors.append([letter, self.green])
            elif letter in answer:
                colors.append([letter, self.yellow])
            else:
                colors.append([letter, self.grey])
        self.round += 1
        self.guess5 = guess5
        return colors


# ####### Numbers ####### #
def create_numbers_divs():
    """
    Generates div info for numbers page.
    Returns 25 divs in random order, containing 1-9 once.
    """
    numbers_divs = [["", ""] for x in range(25)]
    boxes = ["boxB", "boxC", "boxD", "boxE", "boxF", "boxG", "boxH", "boxI"]
    for index, box in enumerate(boxes):
        numbers_divs[index] = [(index + 2), box]
    for div in numbers_divs[8:]:
        div[1] = "boxEmpty"
    random.shuffle(numbers_divs)
    return numbers_divs
