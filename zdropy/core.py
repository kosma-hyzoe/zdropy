import os
import sys
import time
import argparse
import calendar

from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler

from zdropy import config
from zdropy import constants
from zdropy.pages.login import LoginPage
from zdropy.pages.booking import BookingPage
from zdropy.helpers import get_date, get_driver, get_registration_datetime
from zdropy.helpers import is_valid_date, is_valid_time
from zdropy.models import ClassInfo, Credentials, RunParams


def run():
    credentials = get_credentials()
    run_params = get_run_params()

    if not run_params.skip_check:
        check_class(credentials, run_params.class_info)

    registration_datetime = get_registration_datetime(run_params.class_info)

    scheduler = BlockingScheduler()
    scheduler.add_job(book_class, 'date', run_date=registration_datetime,
                      args=[credentials, run_params.class_info, False])
    print("Awaiting booking datetime: " + registration_datetime.strftime('%c'))

    try:
        scheduler.start()
    except EOFError:
        sys.exit(0)


def book_class(credentials, class_info, retry: bool = config.RETRY,
               retry_after_duration: int = config.RETRY_AFTER_DURATION):
    driver = get_driver(config.BROWSER)
    try:
        driver.get(constants.LOGIN_PAGE_URL)
        login_form = LoginPage(driver)
        booking_page = login_form.login(credentials)

        if class_info.club and not booking_page.is_club_selected(class_info):
            booking_page.change_club(class_info)

        try:
            booking_page.book_class(class_info)
            driver.quit()
            return
        except AttributeError:
            if retry:
                print(f"First attempt to book class failed -"
                      f" retrying in {retry_after_duration} seconds...")
                time.sleep(retry_after_duration)
                driver.refresh()
                booking_page = BookingPage(driver)
                booking_page.book_class(class_info)
            else:
                print("Failed to book class.")
                raise AttributeError
    finally:
        driver.quit()


def check_class(credentials, class_info):
    driver = get_driver(config.BROWSER)
    try:
        driver.get(constants.LOGIN_PAGE_URL)
        login_form = LoginPage(driver)
        booking_page = login_form.login(credentials)

        if class_info.club and not booking_page.is_club_selected(class_info):
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
    time_arg = parser.add_argument('time', help="time of the class, formatted as %%H:%%M")
    date_arg = parser.add_argument('date', help="date of the class, formatted as %%Y-%%m-%%d")
    parser.add_argument('--club', '-c', type=str, default=None, help="full club name (case sensitive)")

    parser.add_argument('--skip-check', '-s', action='store_true', help="don't check lesson validity")

    run_params = parser.parse_args()
    if run_params.date.capitalize() in calendar.day_name:
        run_params.date = get_date(run_params.date.capitalize())
    elif not is_valid_date(run_params.date):
        raise argparse.ArgumentError(argument=date_arg, message="Invalid 'date' argument")

    if not is_valid_time(run_params.time):
        raise argparse.ArgumentError(argument=time_arg, message="Invalid 'time' argument")

    class_info = ClassInfo(run_params.name, run_params.time, run_params.date, run_params.club)
    return RunParams(class_info, run_params.skip_check, None)


def get_credentials() -> Credentials:
    load_dotenv()
    return Credentials(os.getenv('LOGIN'), os.getenv('PASSWORD'))


if __name__ == '__main__':
    run()
