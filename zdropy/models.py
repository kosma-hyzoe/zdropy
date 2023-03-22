from collections import namedtuple

LocatorTemplate = namedtuple('Locator', ['By', 'locator'])
ClassInfo = namedtuple('ClassInfo', ['name', 'time', 'date', 'club'])
RunParams = namedtuple('RunParams', ['class_info', 'skip_check', 'weekly'])
Credentials = namedtuple('Credentials', ['login', 'password'])
