import argparse
import os
import sys
import schedule
import calendar
from dotenv import load_dotenv

import config
import constants
from pages.login import LoginPage
from helpers import get_driver, get_date, get_registration_datetime
from helpers import is_valid_date, is_valid_time

from models import ClassInfo, Credentials


def main():
    driver = get_driver(config.BROWSER)
    credentials = get_credentials()
    class_info = get_class_info()
    registration_datetime = get_registration_datetime(class_info, 2)

    if config.CHECK_CLASS_WHEN_SCHEDULING:
        check_class(driver, credentials, class_info)

    schedule.every(config.RETRY_AFTER).seconds.at(registration_datetime).do(
        book_class(driver, credentials, class_info))

    while True:
        try:
            schedule.run_pending()
        except EOFError:
            sys.exit(0)
        except Exception:
            pass


def book_class(driver, credentials, class_info):
    try:
        driver.get(constants.LOGIN_PAGE_URL)
        login_form = LoginPage(driver)
        booking_page = login_form.login(credentials)
        booking_page.ensure_list_view()

        if class_info.club and not booking_page.is_club_selected(class_info):
            booking_page.change_club(class_info)

        booking_page.book_class(class_info)
    finally:
        driver.quit()


def check_class(driver, credentials, class_info):
    try:
        driver.get(constants.LOGIN_PAGE_URL)
        login_form = LoginPage(driver)
        booking_page = login_form.login(credentials)
        booking_page.ensure_list_view()

        if class_info.club and booking_page.is_club_selected(class_info):
            booking_page.change_club(class_info)

        if booking_page.is_class_valid(class_info):
            print("Class check successful.")

    finally:
        driver.quit()
        raise AssertionError("Class check failed - check the provided class info.")


def get_class_info() -> ClassInfo:
    parser = argparse.ArgumentParser()

    parser.add_argument('name', help="name of the class (case sensitive)")
    time_arg = parser.add_argument('time', help='time of the class, formatted as %H:%M')
    date_arg = parser.add_argument('date', help='date of the class, formatted as %Y-%m-%d')
    parser.add_argument('--club', "-c", type=str, default=None, help="full club name (case sensitive)")

    class_info = parser.parse_args()

    if class_info.date.capitalize() in calendar.day_name:
        class_info.date = get_date(class_info.date.capitalize())
    elif not is_valid_date(class_info.date):
        raise argparse.ArgumentError(argument=date_arg, message="Invalid 'date' argument")

    if not is_valid_time(class_info.time):
        raise argparse.ArgumentError(argument=time_arg, message="Invalid 'time' argument")

    return ClassInfo(class_info.name, class_info.time, class_info.date, class_info.club)


def get_credentials() -> Credentials:
    load_dotenv()
    return Credentials(os.getenv('LOGIN'), os.getenv('PASSWORD'))


if __name__ == '__main__':
    main()
