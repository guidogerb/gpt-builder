from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from urllib.parse import urlparse
import time
from load_scraped_urls import load_scraped_urls
from load_queue import load_queue
from update_files import update_files

def scrape_site(start_url, domain, scraped_file, queue_file, chrome_driver_path):
    scraped_urls = load_scraped_urls(scraped_file)
    url_queue = load_queue(queue_file)

    if not scraped_urls:
        url_queue.add(start_url)

    service = Service(executable_path=chrome_driver_path)
    try:
        with webdriver.Chrome(service=service) as browser:
            while url_queue:
                current_url = url_queue.pop()
                if current_url in scraped_urls:
                    continue

                try:
                    browser.get(current_url)
                    time.sleep(3)
                    scraped_urls.add(current_url)

                    links = browser.find_elements(By.TAG_NAME, 'a')
                    new_urls = {link.get_attribute('href') for link in links if link.get_attribute('href') and urlparse(link.get_attribute('href')).netloc == domain}
                    url_queue.update(new_urls)

                    update_files(current_url, url_queue, scraped_file, queue_file)
                except WebDriverException as e:
                    print(f"Error while scraping {current_url}: {e}")

    except WebDriverException as e:
        print(f"Error initializing WebDriver: {e}")
