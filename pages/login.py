from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import Timeout
from debugging import highlight_element
from helpers import get_webdriver_wait


# page_url = about:blank
class LoginForm(object):
    login_input_field_locator = (By.NAME, "Login")
    password_input_field_locator = (By.NAME, "Password")
    log_in_button_locator = (By.XPATH, "//*[@id='confirm' and contains(@text, 'Login')]")

    def __init__(self, driver):
        self.driver = driver

    def login(self, credentials):
        login_input_field = get_webdriver_wait(self.driver, Timeout.MEDIUM).until(
            EC.element_to_be_clickable(self.login_input_field_locator))
        login_input_field.click()
        login_input_field.send_keys(credentials.login)

        password_input_field = self.driver.find_element(*self.password_input_field_locator)
        password_input_field.click()
        password_input_field.send_keys(credentials.password)

        login_button = self.driver.find_element(*self.log_in_button_locator)
        login_button.click()