from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException

def init_domain(domain, driver_path, pages_dir):
    # Attempt to open the site with HTTPS
    start_url_https = f'https://{domain}'
    start_url_http = f'http://{domain}'

    service = Service(executable_path=driver_path)
    try:
        with webdriver.Chrome(service=service) as browser:
            browser.get(start_url_https)
            return start_url_https
    except WebDriverException:
        try:
            with webdriver.Chrome(service=service) as browser:
                browser.get(start_url_http)
                return start_url_http
        except WebDriverException:
            raise Exception(f"Both HTTPS and HTTP protocols failed for {domain}")

