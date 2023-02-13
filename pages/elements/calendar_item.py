from selenium.webdriver.common.by import By


class CalendarItem(object):
    NAME_LOCATOR = (By.CLASS_NAME, 'calendar-item-name')
    START_TIME_LOCATOR = (By.CLASS_NAME, 'calendar-item-start')
    CLASS_ITEM_ACTIONS_LOCATOR = (By.CLASS_NAME, 'class-item-actions')

    def __init__(self, element):
        self.element = element

    def book_or_join_wait_list(self):
        self.element.find_element(*self.CLASS_ITEM_ACTIONS_LOCATOR).click()

    def get_name(self):
        return self.element.find_element(*self.NAME_LOCATOR).text

    def get_start_time(self):
        return self.element.find_element(*self.START_TIME_LOCATOR).text

    def is_bookable(self):
        return True if 'is-bookable' in self.element.get_attribute('class') else False

    def is_awaitable(self):
        return True if 'is-awaitable' in self.element.get_attribute('class') else False

    def is_booked(self):
        return True if 'is-booked' in self.element.get_attribute('class') else False