from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

import config
from models import ClassInfo
from pages.elements.calendar_item import CalendarItem
from pages.page import Page


# page_url = https://zdrofit.perfectgym.pl/ClientPortal2/#/Classes
class BookingPage(Page):
    CHANGE_CLUB_BUTTON_LOCATOR = (By.CLASS_NAME, 'cp-choose-club')
    CALENDAR_ITEM_LOCATOR = (By.CLASS_NAME, 'cp-calendar-item')
    LOGO_LOCATOR = (By.CLASS_NAME, 'cp-header-logo')
    CLUB_SECONDARY_TITLE_LOCATOR = (By.CLASS_NAME, 'secondary-title')

    def __init__(self, driver):
        super().__init__(driver)

    def change_club(self, class_info):
        change_club_button = self.driver.find_element(*self.CHANGE_CLUB_BUTTON_LOCATOR)
        change_club_button.click()

        club_link = self._get_club_calendar_url(class_info.club)
        self.driver.get(club_link)

        return BookingPage(self.driver)

    def ensure_list_view(self):
        if "Calendar" in self.driver.current_url:
            self.driver.get(self.driver.current_url.replace("Calendar", "List"))
        return BookingPage(self.driver)

    def is_club_selected(self, class_info):
        club_secondary_title_element = self.driver.find_element(*self.CLUB_SECONDARY_TITLE_LOCATOR)
        if class_info.club in club_secondary_title_element.text:
            return True
        else:
            return False

    def book_class(self, class_info: ClassInfo):
        calendar_item = self._get_desired_calendar_item(class_info)

        if calendar_item.is_bookable() or (calendar_item.is_awaitable() and config.JOIN_WAIT_LIST):
            calendar_item.book_or_join_wait_list()
        else:
            raise AssertionError("Error when trying to book the class: class is not bookable and/or awaitable")

        if not calendar_item.is_booked():
            raise AssertionError("Error when trying to book the class: can't confirm booking")

    def _get_club_calendar_url(self, club: str) -> str:
        try:
            club_calendar_link = self.driver.find_element(By.XPATH, f"//a[contains(text(), '{club}')]")
            return club_calendar_link.get_attribute("href")
        except NoSuchElementException:
            raise ValueError(f"No club named '{club}' found")

    def is_class_available(self, class_info) -> bool:
        try:
            self._get_desired_calendar_item(class_info)
            return True
        except AssertionError:
            return False

    def _get_desired_calendar_item(self, class_info) -> CalendarItem:
        current_url = self.driver.current_url
        if class_info.date not in current_url:
            date_parameter = current_url[current_url.index("date="):current_url.index("&")]
            self.driver.get(current_url.replace(date_parameter, f"date={class_info.date}"))

        for calendar_item in self._get_calendar_items():
            if calendar_item.get_name() == class_info.name and calendar_item.get_start_time() == class_info.time:
                return calendar_item
        raise AssertionError("Error when trying to locate the calendar item for the class")

    def _get_calendar_items(self) -> list[CalendarItem]:
        calendar_items = self.driver.find_elements(*self.CALENDAR_ITEM_LOCATOR)
        return [CalendarItem(calendar_item) for calendar_item in calendar_items]
