from collections import namedtuple

LocatorTemplate = namedtuple('Locator', ['By', 'locator'])
ClassInfo = namedtuple('ClassInfo', ['name', 'time', 'date', 'club'])
Credentials = namedtuple('Credentials', ['login', 'password'])
RetryAfter = namedtuple("RetryAfter", ['unit', 'value'])

