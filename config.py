import datetime

# supported browser settings: "firefox", "chrome"
BROWSER: str = "chrome"

CHECK_CLASS_WHEN_SCHEDULING: bool = True
# in seconds. set as "None" if you don't want to retry
RETRY: bool = True
RETRY_AFTER_DURATION: int = 60
# in days
REGISTRATION_TIME_DELTA: int = 2 

JOIN_WAIT_LIST: bool = True

# in seconds 
SHORT_TIMEOUT: float = 0.5

DEFAULT_TIMEOUT: float = 5.

LONG_TIMEOUT: float = 5.

DRIVER_OPTIONS: list[str] = [

]
# only for chrome options
DRIVER_EXPERIMENTAL_OPTIONS: list[tuple] = [

]
