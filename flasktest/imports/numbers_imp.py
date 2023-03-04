"""
Handles logic for the countries page.
Handles data and images.
"""

import random


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
