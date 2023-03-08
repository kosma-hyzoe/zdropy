import calendar
import datetime
from selenium import webdriver

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

import config
from constants import DATE_FORMAT
from models import ClassInfo


def get_registration_datetime(class_info: ClassInfo, timedelta_in_days: int = config.REGISTRATION_TIME_DELTA)\
        -> datetime.datetime:
    class_datetime = datetime.datetime.strptime("T".join([class_info.date, class_info.time]), "%Y-%m-%dT%H:%M")
    registration_time_delta = datetime.timedelta(days=timedelta_in_days)
    return class_datetime - registration_time_delta


def get_date(day_of_week: str) -> str:
    today = datetime.datetime.now().date()
    today_weekday = calendar.day_name[today.weekday()]
    if today_weekday == day_of_week:
        return today.strftime(DATE_FORMAT)
    else:
        delta = (7 + calendar.day_name.index(day_of_week) - today.weekday()) % 7
        return (today + datetime.timedelta(days=delta)).strftime(DATE_FORMAT)


def get_driver(browser: str = config.BROWSER):
    if browser == "chrome":
        options = ChromeOptions()
        [options.add_argument(option) for option in config.DRIVER_OPTIONS]
        [options.add_experimental_option(*option) for option in config.DRIVER_EXPERIMENTAL_OPTIONS]
        return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    elif browser == "firefox":
        options = FirefoxOptions()
        [options.add_argument(option) for option in config.DRIVER_OPTIONS]
        return webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)


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
