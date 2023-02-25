from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import NoSuchElementException


class Page(object):
    def __init__(self, driver, timeout: int, element_to_wait_for_locator: (By, str)):
        self.name = self.__class__.__name__
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout)
        self.element_to_wait_for_locator = element_to_wait_for_locator

    def is_displayed(self) -> bool:
        try:
            return self.driver.find_element(*self.element_to_wait_for_locator).is_displayed()
        except NoSuchElementException:
            return False

    def wait_until_is_loaded(self):
        self.wait.until(EC.element_to_be_clickable(self.element_to_wait_for_locator))

    def wait_until_is_closed(self):
        self.wait.until(EC.invisibility_of_element_located(self.element_to_wait_for_locator))
