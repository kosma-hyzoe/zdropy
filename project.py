import argparse
import os
import pickle
import time

import schedule
import sys
import calendar

from dotenv import load_dotenv
import config
import constants
from pages.booking import BookingPage
from pages.login import LoginPage
from helpers import get_date, get_registration_datetime, get_driver
from helpers import is_valid_date, is_valid_time

from models import ClassInfo, Credentials, RunParams


def main():
    credentials = get_credentials()
    run_params = get_run_params()
    registration_datetime = get_registration_datetime(run_params.class_info)

    if not run_params.skip_check:
        check_class(get_driver(), credentials, run_params.class_info)

    if not run_params.weekly:
        pass
    else:
        schedule.every().week.at(str(registration_datetime)).do(
            book_class(get_driver(), credentials, run_params.class_info))
        with open("jobs.pickle", "wb") as f:
            pickle.dump(schedule.jobs, f)


def book_class(driver, credentials, class_info,
               retry: bool = config.RETRY, retry_after_duration: int = config.RETRY_AFTER_DURATION):
    try:
        driver.get(constants.LOGIN_PAGE_URL)
        login_form = LoginPage(driver)
        booking_page = login_form.login(credentials)

        if class_info.club and not booking_page.is_club_selected(class_info):
            booking_page.change_club(class_info)

        try:
            booking_page.book_class(class_info)
        except AttributeError as e:
            if retry:
                time.sleep(retry_after_duration)
                driver.refresh()
                booking_page = BookingPage(driver)
                booking_page.book_class(class_info)
            else:
                raise e
    finally:
        driver.quit()


def check_class(driver, credentials, class_info):
    try:
        driver.get(constants.LOGIN_PAGE_URL)
        login_form = LoginPage(driver)
        booking_page = login_form.login(credentials)

        if class_info.club and booking_page.is_club_selected(class_info):
            booking_page.change_club(class_info)

        if booking_page.is_class_valid(class_info):
            print("Class check successful.")
        else:
            raise AttributeError("Class check failed.")
    finally:
        driver.quit()


def get_run_params() -> RunParams:
    parser = argparse.ArgumentParser()

    parser.add_argument('name', help="name of the class (case sensitive)")
    time_arg = parser.add_argument('time', help="time of the class, formatted as %H:%M")
    date_arg = parser.add_argument('date', help="date of the class, formatted as %Y-%m-%d")
    parser.add_argument('--club', '-c', type=str, default=None, help="full club name (case sensitive)")

    parser.add_argument('--skip-check', '-s', action='store_true', help="don't check lesson validity")
    parser.add_argument('--weekly', '-w', action='store_true', help="schedule weekly")

    run_params = parser.parse_args()
    if run_params.date.capitalize() in calendar.day_name:
        run_params.date = get_date(run_params.date.capitalize())
    elif not is_valid_date(run_params.date):
        raise argparse.ArgumentError(argument=date_arg, message="Invalid 'date' argument")

    if not is_valid_time(run_params.time):
        raise argparse.ArgumentError(argument=time_arg, message="Invalid 'time' argument")

    class_info = ClassInfo(run_params.name, run_params.time, run_params.date, run_params.club)
    return RunParams(class_info, run_params.skip_check, run_params.weekly)


def get_credentials() -> Credentials:
    load_dotenv()
    return Credentials(os.getenv('LOGIN'), os.getenv('PASSWORD'))


if __name__ == '__main__':
    main()
