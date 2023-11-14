import sys
import os
from scrape_site import scrape_site
from selenium.common.exceptions import WebDriverException
from test_protocol import test_protocol

def main(domain):

    script_directory = os.path.dirname(os.path.realpath(__file__))
    chrome_driver_path = os.path.join(script_directory, 'drivers', 'chromedriver-win64', 'chromedriver.exe')

    # Attempt to open the site with HTTPS
    start_url = f'https://{domain}'
    try:
        test_protocol(start_url, chrome_driver_path)
    except WebDriverException:
        # If HTTPS fails, try with HTTP
        start_url = f'http://{domain}'
        try:
            test_protocol(start_url, chrome_driver_path)
        except WebDriverException:
            print(f"Error: Both HTTPS and HTTP protocols failed for {domain}.")
            sys.exit(1)

    scraped_content_dir = os.path.join(os.getcwd(), 'scraped_content')
    output_dir = os.path.join(scraped_content_dir, domain)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    scraped_file = os.path.join(output_dir, 'scraped_urls.txt')
    queue_file = os.path.join(output_dir, 'queue.txt')

    # Check and create scraped_file and queue_file if they don't exist
    for file_path in [scraped_file, queue_file]:
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                pass  # Create the file

    scrape_site(start_url, domain, scraped_file, queue_file, chrome_driver_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <domain>")
    else:
        main(sys.argv[1])
