import calendar
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


TIME_FORMAT = "%H:%M"
DATE_FORMAT = "%Y-%m-%d"


def get_date(day_of_week: str):
    today = datetime.datetime.now().date()
    today_weekday = calendar.day_name[today.weekday()]
    if today_weekday == day_of_week:
        return today.strftime(DATE_FORMAT)
    else:
        delta = (7 + calendar.day_name.index(day_of_week) - today.weekday()) % 7
        return (today + datetime.timedelta(days=delta)).strftime(DATE_FORMAT)


def get_logger():
    pass


def get_driver():
    return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


# todo move to sth like helpers/validators.py if it grows
def is_valid_date(date: str) -> bool:
    try:
        datetime.datetime.strptime(date, DATE_FORMAT)
        return True
    except ValueError:
        return False


def is_valid_time(time: str):
    try:
        datetime.datetime.strptime(time, '%H:%M')
        return True
    except ValueError:
        return False

# todo check_class()?