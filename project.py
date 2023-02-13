import argparse
import os

import schedule
from datetime import datetime
import calendar

from dotenv import load_dotenv

import config
from helpers.helpers import get_driver, get_date, is_valid_date, is_valid_time
from helpers.models import ClassInfo, Credentials
from pages.login import LoginPage


def main():
    class_info = get_class_info()
    driver = get_driver()

    # todo a separate method for this?
    class_datetime = datetime.strptime("T".join([class_info.date, class_info.time]), "%Y-%m-%dT%H:%M")
    registration_datetime = class_datetime - config.REGISTRATION_TIME_DELTA

    if config.RETRY_AFTER.unit == "minutes":
        schedule.every(config.RETRY_AFTER.value).minutes(registration_datetime).do(
            book_class(driver, class_info))
    elif config.RETRY_AFTER.unit == "seconds":
        schedule.every(config.RETRY_AFTER.value).seconds(registration_datetime).do(book_class(driver, class_info))

    # todo prettify
    try:
        while True:
            schedule.run_pending()
    except EOFError:
        pass
    # todo handle cases for registration failure
    except:
        pass


def book_class(driver, credentials, class_info):
    driver.get(config.LOGIN_PAGE_URL)
    login_form = LoginPage(driver)
    booking_page = login_form.login(credentials)
    booking_page.ensure_list_view()

    if class_info.club and booking_page.is_desired_club_selected(class_info):
        booking_page.change_club(class_info)

    booking_page.book_class(class_info)


def get_class_info():
    parser = argparse.ArgumentParser()

    # todo helps
    parser.add_argument('name')
    time_arg = parser.add_argument('time')
    date_arg = parser.add_argument('date')
    parser.add_argument('--club', "-c", type=str, default=None)

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
