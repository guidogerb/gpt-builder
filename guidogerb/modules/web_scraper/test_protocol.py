from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service

def test_protocol(url, driver_path):
    service = Service(executable_path=driver_path)
    try:
        with webdriver.Chrome(service=service) as browser:
            browser.get(url)
    except WebDriverException as e:
        # Handle the WebDriverException
        raise e
