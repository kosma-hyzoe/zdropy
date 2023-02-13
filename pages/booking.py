from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import config
from config import LONG_TIMEOUT
from helpers.models import ClassInfo
from pages.elements.calendar_item import CalendarItem


# page_url = https://zdrofit.perfectgym.pl/ClientPortal2/#/Classes
class BookingPage(object):
    CHANGE_CLUB_BUTTON_LOCATOR = (By.CLASS_NAME, 'cp-choose-club')
    CALENDAR_ITEM_LOCATOR = (By.CLASS_NAME, 'cp-calendar-item')
    LOGO_LOCATOR = (By.CLASS_NAME, 'cp-header-logo')
    CLUB_SECONDARY_TITLE_LOCATOR = (By.CLASS_NAME, 'secondary-title')

    def __init__(self, driver):
        self.driver = driver
        WebDriverWait(self.driver, LONG_TIMEOUT).until(EC.visibility_of_element_located(self.LOGO_LOCATOR))

    def change_club(self, class_info):
        change_club_button = self.driver.find_element(*self.CHANGE_CLUB_BUTTON_LOCATOR)
        change_club_button.click()

        club_link = self._get_club_calendar_url(class_info.club)
        self.driver.get(club_link)

        return BookingPage(self.driver)


    # todo low priority: find a faster club link locator
    def _get_club_calendar_url(self, club: str) -> str:
        club_calendar_link = self.driver.find_element(By.XPATH, f"//a[contains(text(), '{club}')]")
        return club_calendar_link.get_attribute("href")

    def ensure_list_view(self):
        if "Calendar" in self.driver.current_url:
            self.driver.get(self.driver.current_url.replace("Calendar", "List"))
        return BookingPage(self.driver)

    def is_desired_club_selected(self, class_info):
        club_secondary_title_element = self.driver.find_element(*self.CLUB_SECONDARY_TITLE_LOCATOR)
        if class_info.club in club_secondary_title_element.text:
            return True
        else:
            return False

    def book_class(self, class_info: ClassInfo):
        class_calendar_item = self._get_calendar_item(class_info)

        if class_calendar_item.is_bookable() or (class_calendar_item.is_awaitable() and config.JOIN_WAIT_LIST):
            class_calendar_item.book_or_join_wait_list()
        else:
            raise Exception

    def _get_calendar_item(self, class_info) -> CalendarItem:
        current_url = self.driver.current_url
        if class_info.date not in current_url:
            date_parameter = current_url[current_url.index("date="):current_url.index("&")]
            self.driver.get(current_url.replace(date_parameter, f"date={class_info.date}"))

        for calendar_item in self._get_calendar_items():
            if calendar_item.get_name() == class_info.name and calendar_item.get_start_time() == class_info.time:
                return calendar_item
        # todo find suitable exception
        raise Exception

    def _get_calendar_items(self) -> list[CalendarItem]:
        calendar_items = self.driver.find_elements(*self.CALENDAR_ITEM_LOCATOR)
        return [CalendarItem(calendar_item) for calendar_item in calendar_items]
