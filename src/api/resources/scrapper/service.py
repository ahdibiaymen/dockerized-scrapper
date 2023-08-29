import requests
import socket
from flask import current_app
from src.scrapper.selenium_screener import Selenium


class ScrapperService:
    @classmethod
    def snapshot_html(cls, url, follow_redirections=True):
        """
        Download the main (level-0) web page of the given url

        Inputs:
            - url: the url to snapshot

        Output: (HTTP status code, a string containing the html data)
        """
        headers = current_app.config["REQUESTS_HEADERS"]
        try:
            response = requests.get(
                url,
                allow_redirects=follow_redirections,
                headers=headers,
                timeout=current_app.config["SNAPSHOT_HTML_TIMEOUT"],
                verify=False,
            )
        except (requests.exceptions.RequestException, socket.timeout) as ex:
            current_app.logger.warn("Cannot get HTML content (%s) of %s", str(ex), url)
            return 0, b""
        return response.status_code, response.content

    @classmethod
    def take_selenium_snapshot(cls, url, png_path, html_path):
        """
        Take snapshots of the rendered website. Uses Selenium.

        Inputs:
            - url: the url to snapshot
        """
        selenium_scrapper = Selenium(
            private=True,
            headless=True,
            browser=current_app.config["DEFAULT_SELENIUM_BROWSER"],
            enable_proxy=current_app.config["ENABLE_SELENIUM_PROXY"],
            insecure_cert=True,
        )
        selenium_scrapper.take_snapshot(
            url,
            add_initial_page_load_time=False,
            html_path=html_path,
            png_path=png_path,
        )

    @classmethod
    def scrap_url(cls, args):
        status, html = cls.snapshot_html(args["url"])
        cls.take_selenium_snapshot(args["url"], args["png_path"], args["html_path"])
        return status, html
