import pytest

import config
import constants
import testdata
from helpers import get_driver
from pages.login import LoginPage
from project import book_class, get_credentials, check_class


def test_get_credentials():
    try:
        driver = get_driver()
        driver.get(constants.LOGIN_PAGE_URL)
        login_form = LoginPage(driver)
        login_form.login(get_credentials())
    except AttributeError:
        pytest.fail(f"Failed to login with provided credentials.")


def test_check_class():
    try:
        check_class(get_driver(), get_credentials(), testdata.valid_class_info)
    except AttributeError:
        pytest.fail(f"Failed to check class: {testdata.valid_class_info}")
    with pytest.raises(AttributeError):
        check_class(get_driver(), get_credentials(), testdata.invalid_class_info)


def test_book_class():
    # try to book a class
    try:
        book_class(get_driver(), get_credentials(), testdata.valid_class_info, retry=False)
    except AttributeError:
        pytest.fail(f"Failed to book class: {testdata.valid_class_info}")
    # try to book the same class again, expect it to fail
    with pytest.raises(AttributeError):
        book_class(get_driver(), get_credentials(), testdata.valid_class_info, retry=False)



