import random
import time
from logging import getLogger

from flask import current_app
from selenium.common.exceptions import (
    NoAlertPresentException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from seleniumwire import webdriver

logger = getLogger("web_scrapper")


class Selenium:
    def __init__(
        self,
        browser="FIREFOX",
        private=True,
        headless=True,
        insecure_cert=True,
        enable_proxy=False,
    ):
        self.__exit_timeout = current_app.config["BROWSER_EXIT_TIMEOUT"]
        self.__OCD_PROXY = current_app.config.get("PROXY_HOST", None)
        self.__username = current_app.config.get("PROXY_USERNAME", None)
        self.__password = current_app.config.get("PROXY_PASSWORD", None)

        if browser.upper() == "FIREFOX":
            self.driver = self.generate_firefox_driver(
                private, headless, insecure_cert, enable_proxy
            )
        elif browser.upper() == "CHROME":
            self.driver = self.generate_chrome_driver(
                private, headless, insecure_cert, enable_proxy
            )
        self.driver.delete_all_cookies()
        self.driver.set_window_size(
            width=current_app.config["SNAPSHOT_BROWSER_WINDOW_WIDTH"],
            height=current_app.config["SNAPSHOT_BROWSER_WINDOW_HEIGHT"],
        )

    def __get_ocd_proxy(self):
        if not any([self.__username, self.__password, self.__OCD_PROXY]):
            raise ValueError(
                "The scrapper require proxy config to use it in proxy mode"
            )
        http = (
            "http://"
            + self.__username
            + ":"
            + self.__password
            + "@"
            + self.__OCD_PROXY
        )
        https = (
            "https://"
            + self.__username
            + ":"
            + self.__password
            + "@"
            + self.__OCD_PROXY
        )
        no_proxy = "localhost,127.0.0.1,dev_server:8080"
        proxy_options = {
            "proxy": {
                "http": http,
                "https": https,
                "no_proxy": no_proxy,
            }
        }
        return proxy_options

    def generate_chrome_driver(
        self,
        private=False,
        headless=False,
        insecure_certs=False,
        enable_proxy=False,
    ):
        chromium_options = webdriver.ChromeOptions()
        if headless:
            chromium_options.add_argument("-headless")

        if insecure_certs:
            chromium_options.accept_insecure_certs = True

        if private:
            chromium_options.add_argument("−−incognito")

        executable_path = current_app.config["CHROME_EXECUTABLE_PATH"]
        if enable_proxy:
            proxy_options = self.__get_ocd_proxy()
            driver = webdriver.Chrome(
                service=ChromeService(executable_path),
                seleniumwire_options=proxy_options,
                options=chromium_options,
            )

        else:
            driver = webdriver.Chrome(
                service=ChromeService(executable_path),
                options=chromium_options,
            )

        return driver

    def generate_firefox_driver(
        self,
        private=False,
        headless=False,
        insecure_certs=False,
        enable_proxy=False,
    ):
        firefox_options = webdriver.FirefoxOptions()
        if headless:
            firefox_options.add_argument("-headless")

        if insecure_certs:
            firefox_options.accept_insecure_certs = True

        if private:
            firefox_options.add_argument("-private")

        executable_path = current_app.config["FIREFOX_EXECUTABLE_PATH"]

        if enable_proxy:
            proxy_options = self.__get_ocd_proxy()
            driver = webdriver.Firefox(
                service=FirefoxService(executable_path),
                seleniumwire_options=proxy_options,
                options=firefox_options,
            )

        else:
            driver = webdriver.Firefox(
                service=FirefoxService(executable_path),
                options=firefox_options,
            )

        return driver

    def is_webdriver_alive(self):
        if self.driver is None:
            return False

        try:
            return_code = self.driver.process.poll()
        except WebDriverException as e:
            logger.warning(
                f"Driver is not running due to the following exception : {e}"
            )
            return False
        else:
            return return_code is None

    def take_snapshot(
        self,
        url="https://www.google.com",
        add_initial_page_load_time=False,
        html_path=None,
        png_path=None,
    ):
        if not all((html_path, png_path)):
            raise ValueError(
                "HTML and PNG paths are required for the scrapper !"
            )

        self.driver.get(url)

        if add_initial_page_load_time:
            loading_time = random.randint(
                current_app.config["INITIAL_PAGE_LOAD_TIME_MIN"],
                current_app.config["INITIAL_PAGE_LOAD_TIME_MAX"],
            )
            logger.info(
                f"initial wait of {loading_time} seconds for page loading ...."
            )
            time.sleep(loading_time)

        # TIMEOUT TO EXIT THE PAGE
        wait = WebDriverWait(self.driver, self.__exit_timeout)
        wait.until(
            expected_conditions.visibility_of_element_located(
                (By.TAG_NAME, "body")
            )
        )

        # accept any alert
        try:
            self.driver.switch_to.alert.accept()
        except NoAlertPresentException:
            pass

        try:
            # HTML content snapshot
            html = self.driver.page_source
            with open(html_path, "w+") as fd:
                fd.write(html)
                fd.close()

            # SCREENSHOT
            S = lambda X: self.driver.execute_script(
                "return document.body.parentNode.scroll" + X
            )
            self.driver.set_window_size(S("Width"), S("Height"))
            body = self.driver.find_element(By.TAG_NAME, "body")

            status = body.screenshot(png_path)

            if not status:
                logger.info(
                    "something went wrong while taking '"
                    + url
                    + "' screenshot !, "
                    + "Selenium scrapper cannot save the image to path: "
                    + png_path
                )
            self.driver.quit()
        except TimeoutException:
            logger.info(
                "timout exceeded ! the website didn't load after "
                + self.__exit_timeout
                + " seconds ... exiting"
            )
            self.driver.quit()
