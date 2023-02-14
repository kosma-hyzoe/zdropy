import pytest

import constants
from models import ClassInfo
from helpers import get_driver
from project import book_class, get_credentials


def test_validators():
    ...


@pytest.mark.parametrize("browser", constants.SUPPORTED_BROWSERS)
def test_calendar_page_displays_on_all_supported_browsers(browser):
    driver = get_driver(browser)
    book_class(driver, credentials=get_credentials(), class_info=None)