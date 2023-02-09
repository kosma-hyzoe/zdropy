import pytest

from pages.login import LoginPage
from models import Credentials
from helpers import get_driver, get_credentials


def test_login():
    driver = get_driver()
    driver.get("https://zdrofit.perfectgym.pl/ClientPortal2/#/Login")

    credentials = get_credentials()
    login_form = LoginPage(driver)
    login_form.login(credentials)
    print("foobar")


