"""
Handles logic for the wordle and play_wordle pages.
Handles game logic, saving, loading.
"""

import pandas as pd


class Wordle:
    """
    Class containing wordle game info.
    """
    df_words = pd.read_csv("flasktest/static/data/games/wordle/5_letter_words.csv")
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
