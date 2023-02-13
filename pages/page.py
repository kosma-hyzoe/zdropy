from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from config import LONG_TIMEOUT


class Page(object):

    def __init__(self, driver):
        self.driver = driver
        self._wait_for_body()

    def _wait_for_body(self):
        WebDriverWait(self.driver, LONG_TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, "//body")))
