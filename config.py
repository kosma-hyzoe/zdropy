import datetime

from helpers.models import RetryAfter

REGISTRATION_TIME_DELTA = datetime.timedelta(days=2)
RETRY_AFTER = RetryAfter("minutes", 2)
JOIN_WAIT_LIST = True

LOGIN_PAGE_URL = "https://zdrofit.perfectgym.pl/ClientPortal2/#/Login"

SHORT_TIMEOUT = 0.5
MEDIUM_TIMEOUT = 5.
LONG_TIMEOUT = 5.



OPTIONS = [

]

EXPERIMENTAL_OPTIONS = [

]



