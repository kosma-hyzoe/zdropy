import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

from config import Timeout
from models import Credentials


def get_webdriver_wait(driver, timeout: Timeout) -> WebDriverWait:
    return WebDriverWait(driver, timeout.value)


def get_logger():
    pass


def get_driver():
    return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


def get_credentials() -> Credentials:
    load_dotenv()
    return Credentials(os.getenv("LOGIN"), os.getenv("PASSWORD"))

