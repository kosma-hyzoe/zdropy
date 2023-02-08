from selenium.webdriver.common.by import By


# page_url = about:blank
class LoginForm(object):
    login_input_field_locator = (By.NAME, "Login")

    def __init__(self, driver):
        self.driver = driver

    def login(self, login):
        login_input_field = self.driver.find_element(self.login_input_field_locator)
        login_input_field.click()
        login_input_field.send_keys(login)



