import sys
import os
from scrape_site import scrape_site
from selenium.common.exceptions import WebDriverException
from test_protocol import test_protocol
from init_domain import init_domain
import argparse

def main(args):

    script_directory = os.path.dirname(os.path.realpath(__file__))
    if(args.driver_path):
        chrome_driver_path = args.driver_path
    else:
        chrome_driver_path = os.path.join(script_directory, 'drivers', 'chromedriver-win64', 'chromedriver.exe')

    scraped_content_dir = os.path.join(os.getcwd(), 'scraped_content')
    output_dir = os.path.join(scraped_content_dir, args.domain)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    scraped_file = os.path.join(output_dir, 'scraped_urls.txt')
    queue_file = os.path.join(output_dir, 'queue.txt')

    # Check and create scraped_file and queue_file if they don't exist
    for file_path in [scraped_file, queue_file]:
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                pass  # Create the file

    # Create/check for 'pages' subdirectory
    pages_dir = os.path.join(output_dir, 'pages')
    if not os.path.exists(pages_dir):
        os.makedirs(pages_dir)

    # Initialize the domain
    try:
        start_url = init_domain(args.domain, chrome_driver_path, pages_dir)
    except Exception as e:
        print(e)
        sys.exit(1)

    if(args.execute_scrape):
        # Scrape the site
        print(f"Starting scrape for {args.domain}")
        scrape_site(start_url, args.domain, scraped_file, queue_file, chrome_driver_path)

if __name__ == "__main__":
    # Init arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--driver_path', help='Path to the chromedriver executable', default=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'drivers', 'chromedriver-win64', 'chromedriver.exe'))
    parser.add_argument('--domain', help='Domain to scrape')
    parser.add_argument('--execute_scrape', help='Execute the scrape', default=False)
    args = parser.parse_args()
    main(args)