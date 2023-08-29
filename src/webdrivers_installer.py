import os
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from webdriver_manager.firefox import GeckoDriverManager

DRIVERS_ENV_FILE = "/tmp/web-drivers"


def install_web_drivers():
    webdriver_installers = {
        "chrome": ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install,
        "firefox": GeckoDriverManager().install,
    }
    with open(f"{DRIVERS_ENV_FILE}", "a+") as file:
        for webdriver_name in webdriver_installers.keys():
            try:
                print(f"[INFO] Installing {webdriver_name} web driver")
                if os.environ.get(f"{webdriver_name}_EXECUTABLE_PATH") is None:
                    path = webdriver_installers[webdriver_name]()
                    file.write(f"{webdriver_name.upper()}_EXECUTABLE_PATH={path}\n")
                    print(f"[INFO] {webdriver_name} web driver successfully installed!")
            except Exception as e:
                print(
                    "[ERROR] Something went wrong "
                    "while installing {} web driver due"
                    " to the following exception {}".format(webdriver_name, e)
                )


if __name__ == "__main__":
    install_web_drivers()
