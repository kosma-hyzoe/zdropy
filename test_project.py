from helpers.models import ClassInfo
from helpers import get_driver, get_credentials
from project import book_class


def test_login():
    driver = get_driver()
    credentials = get_credentials()
    class_info = ClassInfo("Zdrofit Bemowo", "foo", "bar", "foobar")
    book_class(driver, credentials, class_info)

