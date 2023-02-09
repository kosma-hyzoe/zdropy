from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def highlight_element(driver, element):
    original_style = element.get_attribute("style")
    driver.execute_script("arguments[0].setAttribute(arguments[1], arguments[2])",
                          element,
                          "style",
                          "border: 2px solid red;")