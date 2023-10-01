import os
from pathlib import Path
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

ROOT_PATH = Path(__file__).parent.parent.parent

CRHOMEDRIVER_NAME = 'chromedriver.exe'
CRHOMEDRIVER_PATH = ROOT_PATH / 'chromedriver' / CRHOMEDRIVER_NAME


def make_chrome_browser(*options):
    chrome_options = webdriver.ChromeOptions()
    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    if os.environ.get('SELENIUM_HEADLESS') == '1':
        chrome_options.add_argument('--headless')

    chrome_service = Service(executable_path=CRHOMEDRIVER_PATH)
    # chrome_options.add_experimental_option("detach", True)
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return browser


if __name__ == '__main__':
    browser = make_chrome_browser()
    browser.get('https://www.galeriadometeorito.com/')
    sleep(5)
    browser.quit()
