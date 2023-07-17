from dotenv import load_dotenv
from logging.config import dictConfig

load_dotenv(dotenv_path=".env")


class DefaultConfig:
    BROWSER_EXIT_TIMEOUT = 60
    PROXY_HOST = None
    PROXY_USERNAME = None
    PROXY_PASSWORD = None
    ENABLE_SELENIUM_PROXY = False
    SNAPSHOT_BROWSER_WINDOW_WIDTH = 800
    SNAPSHOT_BROWSER_WINDOW_HEIGHT = 1200
    INITIAL_PAGE_LOAD_TIME_MIN = 5
    INITIAL_PAGE_LOAD_TIME_MAX = 15
    DEFAULT_SELENIUM_BROWSER = "firefox"

    @staticmethod
    def init_loggers():
        LOGGING = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "verbose": {
                    "format": (
                        "%(levelname)s -- %(asctime)s --"
                        " %(pathname)s:%(lineno)d >  %(message)s "
                    ),
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },
            "handlers": {
                "console": {
                    "level": "DEBUG",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                    "formatter": "verbose",
                },
                "file": {
                    "level": "INFO",
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": "/tmp/dockerized_scrapper.log",
                    "mode": "a",
                    "maxBytes": 10485760,
                    "backupCount": 10,
                    "formatter": "verbose",
                },
            },
            "loggers": {
                "scrapper": {
                    "level": "INFO",
                    "handlers": ["console", "file"],
                },
            },
        }
        dictConfig(LOGGING)
