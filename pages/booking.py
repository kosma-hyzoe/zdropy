import time

from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import config
from models import ClassInfo
from pages.elements.calendar_item import CalendarColumn
from pages.page import Page


class BookingPage(Page):
    CHANGE_CLUB_BUTTON_LOCATOR = (By.CLASS_NAME, 'cp-choose-club')
    ANY_CATEGORY_FILTER_LOCATOR = (By.XPATH, "//span[contains(text(), 'Any category')]")
    CALENDAR_ITEM_LOCATOR = (By.CLASS_NAME, 'cp-class-list-day-col')
    CLUB_SECONDARY_TITLE_LOCATOR = (By.XPATH, "//span[contains(@class, 'secondary-title')]")
    LIST_VIEW_BUTTON_LOCATOR = (By.XPATH, "//span[contains(@class, 'glyphicon-cp-list')]")

    def __init__(self, driver, timeout: int = config.DEFAULT_TIMEOUT):
        super().__init__(driver, timeout, self.ANY_CATEGORY_FILTER_LOCATOR)
        self.wait_until_is_loaded()

    def change_club(self, class_info) -> "BookingPage":
        change_club_button = self.wait.until(EC.visibility_of_element_located(self.CHANGE_CLUB_BUTTON_LOCATOR))
        change_club_button.click()

        club_link = self._get_club_calendar_url(class_info.club)
        self.driver.get(club_link)

        return BookingPage(self.driver)

    def ensure_list_view(self) -> "BookingPage":
        if "Calendar" in self.driver.current_url:
            self.driver.get(self.driver.current_url.replace("Calendar", "List"))
        return BookingPage(self.driver)

    def is_club_selected(self, class_info) -> bool:
        club_secondary_title_element = self.wait.until(
            EC.visibility_of_element_located(self.CLUB_SECONDARY_TITLE_LOCATOR))
        if class_info.club in club_secondary_title_element.text:
            return True
        else:
            return False

    def book_class(self, class_info: ClassInfo, join_wait_list: bool = config.JOIN_WAIT_LIST) -> "BookingPage":
        self.ensure_list_view()
        self._change_date(class_info)
        self.wait_until_is_loaded()
        calendar_item = self._get_desired_calendar_item(class_info)

        self.wait_until_is_loaded()
        if calendar_item.is_bookable() or (calendar_item.is_awaitable() and join_wait_list):
            calendar_item.book_or_join_wait_list()
        else:
            raise AttributeError

        self.driver.refresh()
        self.wait_until_is_loaded()

        if not self._get_desired_calendar_item(class_info).is_booked():
            if join_wait_list and calendar_item.is_awaiting():
                print("Wait list joined.")
            else:
                raise AttributeError
        else:
            print("Class booked successfully.")
        return BookingPage(self.driver)

    def is_class_valid(self, class_info) -> bool:
        self.ensure_list_view()
        self._change_date(class_info)
        self.wait_until_is_loaded()
        try:
            self._get_desired_calendar_item(class_info)
            return True
        except AttributeError:
            return False

    def wait_until_is_loaded(self):
        self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "baf-load-mask-spinner")))
        self.wait.until(EC.visibility_of_element_located(self.ANY_CATEGORY_FILTER_LOCATOR))

    def _get_club_calendar_url(self, club: str) -> str:
        try:
            club_calendar_link = self.wait.until(EC.visibility_of_element_located((
                By.XPATH, f"//a[contains(text(), '{club}')]")))
            return club_calendar_link.get_attribute("href")
        except NoSuchElementException:
            raise ValueError(f"No club named '{club}' found")

    def _change_date(self, class_info) -> "BookingPage":
        current_url = self.driver.current_url
        if class_info.date not in current_url:
            if "date=" in current_url:
                date_parameter = current_url[current_url.index("date="):current_url.index("&")]
                self.driver.get(current_url.replace(date_parameter, f"date={class_info.date}"))
            else:
                self.driver.get(current_url + "?date=" + class_info.date)
        return BookingPage(self.driver)

    def _get_desired_calendar_item(self, class_info) -> CalendarColumn:
        for calendar_item in self._get_calendar_items():
            if calendar_item.get_name() == class_info.name and calendar_item.get_start_time() == class_info.time:
                return calendar_item

        raise AttributeError("Error when trying to locate the calendar item for the class")

    def _get_calendar_items(self) -> list[CalendarColumn]:
        calendar_items = self.driver.find_elements(*self.CALENDAR_ITEM_LOCATOR)
        return [CalendarColumn(calendar_item) for calendar_item in calendar_items]
