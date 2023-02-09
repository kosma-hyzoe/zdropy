from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from config import Timeout
from helpers import get_webdriver_wait
from pages.booking import BookingPage


# page_url = https://zdrofit.perfectgym.pl/ClientPortal2/#/Login
class LoginPage(object):
    login_input_field_locator = (By.NAME, "Login")
    password_input_field_locator = (By.NAME, "Password")
    log_in_button_locator = (By.XPATH, "//*[@id='confirm' and contains(@text, 'Login')]")

    def __init__(self, driver):
        self.driver = driver

    # todo make a method for switching languages if needed because of the poor login button locator
    def login(self, credentials) -> BookingPage:
        login_input_field = get_webdriver_wait(self.driver, Timeout.MEDIUM).until(
            EC.element_to_be_clickable(self.login_input_field_locator))
        login_input_field.click()
        login_input_field.send_keys(credentials.login)

        password_input_field = self.driver.find_element(*self.password_input_field_locator)
        password_input_field.click()
        password_input_field.send_keys(credentials.password)

        login_button = self.driver.find_element(*self.log_in_button_locator)
        login_button.click()
        return BookingPage(self.driver)
