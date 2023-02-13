from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from config import MEDIUM_TIMEOUT
from pages.booking import BookingPage
from pages.page import Page


# page_url = https://zdrofit.perfectgym.pl/ClientPortal2/#/Login
class LoginPage(Page):
    login_input_field_locator = (By.NAME, "Login")
    password_input_field_locator = (By.NAME, "Password")
    log_in_button_locator = (By.XPATH, "//*[@id='confirm' and contains(@text, 'Login')]")

    def __init__(self, driver):
        super().__init__(driver)

    def login(self, credentials) -> BookingPage:
        login_input_field = WebDriverWait(self.driver, MEDIUM_TIMEOUT).until(
            EC.element_to_be_clickable(self.login_input_field_locator))
        login_input_field.click()
        login_input_field.send_keys(credentials.login)

        password_input_field = self.driver.find_element(*self.password_input_field_locator)
        password_input_field.click()
        password_input_field.send_keys(credentials.password)

        login_button = self.driver.find_element(*self.log_in_button_locator)
        login_button.click()
        return BookingPage(self.driver)
