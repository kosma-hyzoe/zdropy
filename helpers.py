from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def get_logger():
    pass


def get_driver():
    return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


def get_credentials():
    pass
