import argparse
import schedule
from datetime import datetime

from config import *
from helpers import get_driver
# todo implement proper docstrings


def main():
    # todo accept weekdays instead of full dates
    lesson = get_lesson_from_command_line_args()
    # todo specify firefox or chrome in config.py
    driver = get_driver()

    check_lesson(driver, lesson)

    lesson_datetime = datetime.strptime(lesson.datetime, "%m-%dT%H:%M")
    registration_datetime = lesson_datetime - REGISTRATION_TIME_DELTA

    # todo implement namedtuple, get load retry_after from config
    retry_after = ("minutes", 10)
    if retry_after[0] == "minutes":
        schedule.every(retry_after[1]).minutes(registration_datetime).do(register(driver, lesson))
    elif retry_after[0] == "seconds":
        pass

    try:
        while True:
            schedule.run_pending()
    except EOFError:
        pass
    # todo handle cases for registration failure
    except:
        pass


def register(driver, lesson):
    pass


def check_lesson(driver, lesson):
    # todo implement checking if given lesson exist and is "bookable"
    pass


def get_lesson_from_command_line_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("lesson_name")
    parser.add_argument("club_name")
    # todo verify datetime with a helper method
    parser.add_argument("datetime")
    # todo consider a flag to disable lesson checking

    try:
        return parser.parse_args()
    except:
        pass


if __name__ == '__main__':
    main()
