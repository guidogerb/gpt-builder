from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import zipfile
import os
import time

def create_html(url, html_path, driver_path):
    # Setup Selenium WebDriver
    service = Service(executable_path=driver_path)
    with webdriver.Chrome(service=service) as browser:
        browser.get(url)
        time.sleep(5)  # Wait for JavaScript to load. Adjust time as necessary.

        # Fetch fully rendered HTML
        rendered_html = browser.page_source

    # Save HTML content to the specified path
    with open(html_path, 'w', encoding='utf-8') as file:
        file.write(rendered_html)

    # Zip the HTML file
    with zipfile.ZipFile(html_path + '.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(html_path, os.path.basename(html_path))

    # Optionally, delete the original HTML file after zipping
    os.remove(html_path)

# Example usage
# create_html('http://example.com', '/path/to/output/example_com.html', 'path/to/chromedriver')
