import datetime

CHECK_CLASS_WHEN_SCHEDULING: bool = True
# in seconds
RETRY_AFTER: int = 2 * 60

REGISTRATION_TIME_DELTA: datetime.timedelta = datetime.timedelta(days=2)

JOIN_WAIT_LIST: bool = True

SHORT_TIMEOUT: float = 0.5

MEDIUM_TIMEOUT: float = 5.

LONG_TIMEOUT: float = 5.

OPTIONS: list[str] = [

]

EXPERIMENTAL_OPTIONS: list[str] = [

]
