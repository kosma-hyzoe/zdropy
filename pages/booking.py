from selenium.webdriver.common.by import By


# page_url = https://zdrofit.perfectgym.pl/ClientPortal2/#/Classes
class BookingPage(object):
    def __init__(self, driver):
        self.driver = driver
