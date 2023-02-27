from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import config
from pages.booking import BookingPage
from pages.page import Page


class LoginPage(Page):
    LOGIN_INPUT_FIELD_LOCATOR = (By.NAME, "Login")
    PASSWORD_INPUT_FIELD_LOCATOR = (By.NAME, "Password")
    LOG_IN_BUTTON_LOCATOR = (By.XPATH, "//*[@id='confirm' and contains(@text, 'Login')]")

    def __init__(self, driver, timeout: int = config.DEFAULT_TIMEOUT):
        super().__init__(driver, timeout, self.LOGIN_INPUT_FIELD_LOCATOR)

    def login(self, credentials) -> BookingPage:
        login_input_field = self.wait.until(EC.element_to_be_clickable(self.LOGIN_INPUT_FIELD_LOCATOR))
        login_input_field.click()
        login_input_field.send_keys(credentials.login)

        password_input_field = self.driver.find_element(*self.PASSWORD_INPUT_FIELD_LOCATOR)
        password_input_field.click()
        password_input_field.send_keys(credentials.password)

        login_button = self.driver.find_element(*self.LOG_IN_BUTTON_LOCATOR)
        login_button.click()
        return BookingPage(self.driver)
