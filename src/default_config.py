#!/usr/bin/env python
# encoding: utf-8

import os
from logging.config import dictConfig

from dotenv import load_dotenv


class DefaultConfig:
    load_dotenv(dotenv_path=".env")

    DEBUG = os.environ["DEBUG"]
    BUNDLE_ERRORS = True

    PREFIX_PATH = "/{}".format(os.environ["DEPLOYMENT_VERSION"])

    PROPAGATE_EXCEPTIONS = True

    INSTANCE_PATH = os.environ["INSTANCE_PATH"]
    SNAPSHOTS_PATH = os.environ["SNAPSHOTS_PATH"]

    REQUESTS_HEADERS = {
        "User-agent": (
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36"
        ),
    }

    SNAPSHOT_HTML_TIMEOUT = int(os.environ["SNAPSHOT_HTML_TIMEOUT"])

    # Selenium config
    BROWSER_EXIT_TIMEOUT = 60
    SNAPSHOT_BROWSER_WINDOW_HEIGHT = 800
    SNAPSHOT_BROWSER_WINDOW_WIDTH = 1200
    DEFAULT_SELENIUM_BROWSER = os.environ["DEFAULT_SELENIUM_BROWSER"]
    ENABLE_SELENIUM_PROXY = False
    INITIAL_PAGE_LOAD_TIME_MIN = 5
    INITIAL_PAGE_LOAD_TIME_MAX = 15
    # ROUND-ROBIN PROXY
    PROXY_HOST = os.environ["PROXY_HOST"]
    PROXY_USERNAME = os.environ["PROXY_USERNAME"]
    PROXY_PASSWORD = os.environ["PROXY_PASSWORD"]

    # web drivers executable PATHS
    # automatically assigned before the first request
    FIREFOX_EXECUTABLE_PATH = os.environ["FIREFOX_EXECUTABLE_PATH"]
    CHROME_EXECUTABLE_PATH = os.environ["CHROME_EXECUTABLE_PATH"]

    @staticmethod
    def init_loggers():
        LOGGING = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "verbose": {
                    "format": (
                        "%(levelname)s -- %(asctime)s -- %(pathname)s:%(lineno)d >  %(message)s "
                    ),
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },
            "handlers": {
                "console": {
                    "level": "DEBUG",
                    "class": "logging.StreamHandler",
                    "stream": "ext://flask.logging.wsgi_errors_stream",
                    "formatter": "verbose",
                },
                "file": {
                    "level": "INFO",
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": "/tmp/web_scrapper.log",
                    "mode": "a",
                    "maxBytes": 10485760,
                    "backupCount": 10,
                    "formatter": "verbose",
                },
            },
            "loggers": {
                "web_scrapper": {
                    "level": "INFO",
                    "handlers": ["console", "file"],
                },
                "flask_restx": {
                    "level": "INFO",
                    "handlers": ["console", "file"],
                },
            },
        }
        dictConfig(LOGGING)
