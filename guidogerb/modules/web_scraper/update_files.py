def update_files(current_url, new_urls, scraped_file, queue_file):
    with open(scraped_file, 'a') as scraped:
        scraped.write(current_url + '\n')
    with open(queue_file, 'w') as queue:
        for url in new_urls:
            queue.write(url + '\n')
