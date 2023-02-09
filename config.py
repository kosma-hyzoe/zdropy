import datetime
from enum import Enum


class Timeout(Enum):
    SHORT = 0.5
    MEDIUM = 2.
    LONG = 5.


REGISTRATION_TIME_DELTA = datetime.timedelta(days=2)
RETRY_AFTER = (10, "seconds")



