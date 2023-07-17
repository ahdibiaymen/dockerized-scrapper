import random
import time
from logging import getLogger

from selenium.common.exceptions import (
    NoAlertPresentException,
    TimeoutException,
    WebDriverException,
)
from default_config import DefaultConfig
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from webdriver_manager.firefox import GeckoDriverManager

logger = getLogger("pi_celery")


class Selenium:
    def __init__(
            self,
            browser="FIREFOX",
            private=True,
            headless=True,
            insecure_cert=True,
            enable_proxy=False,
    ):
        self.__exit_timeout = DefaultConfig.BROWSER_EXIT_TIMEOUT
        self.__PROXY = DefaultConfig.PROXY_HOST
        self.__username = DefaultConfig.PROXY_USERNAME
        self.__password = DefaultConfig.PROXY_PASSWORD

        if browser == "FIREFOX":
            self.driver = self.generate_firefox_driver(
                private, headless, insecure_cert, enable_proxy
            )
        elif browser == "CHROME":
            self.driver = self.generate_chrome_driver(
                private, headless, insecure_cert, enable_proxy
            )
        self.driver.delete_all_cookies()
        self.driver.set_window_size(
            width=DefaultConfig.SNAPSHOT_BROWSER_WINDOW_WIDTH,
            height=DefaultConfig.SNAPSHOT_BROWSER_WINDOW_HEIGHT,
        )

    def __get_proxy(self):
        if not any([self.__username, self.__password, self.__PROXY]):
            raise ValueError(
                "The scrapper require proxy config to use it in proxy mode"
            )
        http = "http://" + self.__username + ":" + self.__password + "@" + self.__PROXY
        https = "https://" + self.__username + ":" + self.__password + "@" + self.__PROXY
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
            block_popups=False,
    ):
        chromium_options = webdriver.ChromeOptions()
        desired_caps = {}

        if headless:
            chromium_options.add_argument("-headless")

        if insecure_certs:
            chromium_options.accept_insecure_certs = True

        if private:
            chromium_options.add_argument("−−incognito")

        if block_popups:
            desired_caps["goog:chromeOptions"] = {
                "excludeSwitches": ["disable-popup-blocking"]
            }

        executable_path = ChromeDriverManager(
            chrome_type=ChromeType.CHROMIUM
        ).install()
        if enable_proxy:
            proxy_options = self.__get_proxy()
            driver = webdriver.Chrome(
                executable_path=executable_path,
                seleniumwire_options=proxy_options,
                desired_capabilities=desired_caps,
                options=chromium_options,
            )

        else:
            driver = webdriver.Chrome(
                executable_path=executable_path,
                desired_capabilities=desired_caps,
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

        executable_path = GeckoDriverManager().install()

        if enable_proxy:
            proxy_options = self.__get_proxy()
            driver = webdriver.Firefox(
                executable_path=executable_path,
                seleniumwire_options=proxy_options,
                options=firefox_options,
            )

        else:
            driver = webdriver.Firefox(
                executable_path=executable_path,
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
                DefaultConfig.INITIAL_PAGE_LOAD_TIME_MIN,
                DefaultConfig.INITIAL_PAGE_LOAD_TIME_MAX,
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
            with open(html_path, "w") as fd:
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


