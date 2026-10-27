# Date helpers for DD-MM-YYYY dates.
# Only get_today() uses the standard 'time' module (approved), just to read today's date.

import time

MIN_YEAR = 2000
MAX_YEAR = 2100


def is_leap_year(year):
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    if year % 4 == 0:
        return True
    return False


def days_in_month(month, year):
    if month == 2:
        if is_leap_year(year):
            return 29
        return 28
    if month == 4 or month == 6 or month == 9 or month == 11:
        return 30
    return 31


def all_digits(text):
    if text == "":
        return False

    for ch in text:
        if ch not in "0123456789":
            return False

    return True


def is_valid_date(text):
    # Accepts only DD-MM-YYYY with a real calendar date.
    if len(text) != 10:
        return False

    if text[2] != "-" or text[5] != "-":
        return False

    day_text = text[0:2]
    month_text = text[3:5]
    year_text = text[6:10]

    if not (all_digits(day_text) and all_digits(month_text) and all_digits(year_text)):
        return False

    day = int(day_text)
    month = int(month_text)
    year = int(year_text)

    if year < MIN_YEAR or year > MAX_YEAR:
        return False

    if month < 1 or month > 12:
        return False

    if day < 1 or day > days_in_month(month, year):
        return False

    return True


def date_to_number(text):
    # Number of days since 01-01-2000. The date must already be valid.
    day = int(text[0:2])
    month = int(text[3:5])
    year = int(text[6:10])
    total = 0

    for y in range(MIN_YEAR, year):
        if is_leap_year(y):
            total = total + 366
        else:
            total = total + 365

    for m in range(1, month):
        total = total + days_in_month(m, year)

    total = total + day - 1
    return total


def days_between(start_text, end_text):
    return date_to_number(end_text) - date_to_number(start_text)


def ask_date(prompt):
    # Returns a valid date string, or "" if the user types B to go back.
    while True:
        text = input(prompt + " (DD-MM-YYYY, or B to go back): ").strip()

        if text.lower() == "b":
            return ""

        if is_valid_date(text):
            return text

        print("Invalid date. Use DD-MM-YYYY, e.g. 05-03-2026.")


def get_today():
    # Today's date from the computer clock, as DD-MM-YYYY.
    t = time.localtime()
    day = str(t[2])
    month = str(t[1])

    if len(day) == 1:
        day = "0" + day

    if len(month) == 1:
        month = "0" + month

    return day + "-" + month + "-" + str(t[0])
