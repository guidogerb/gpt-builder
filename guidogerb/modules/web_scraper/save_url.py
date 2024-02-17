import os
import zipfile
# Additional imports may be necessary for HTML and PDF saving

def save_url(url, pages_dir,driver_path):
    # Check if the URL is an internal anchor link or ends with an anchor
    if '#' in url:
        return

    # Construct file paths without '.zip'
    url_filename = url.replace('http://', '').replace('https://', '').replace('/', '_')
    html_path = os.path.join(pages_dir, f'{url_filename}.html')
    pdf_page_path = os.path.join(pages_dir, f'{url_filename}.page.pdf')

    # Check for existing files
    if not os.path.exists(html_path + '.zip'):
        create_html(url, html_path)
    if not os.path.exists(pdf_page_path + '.zip'):
        create_pdf_page(url, pdf_page_path)

    # Verify the existence of both files
    assert os.path.exists(html_path + '.zip'), f"Missing HTML zip file for {url}"
    assert os.path.exists(pdf_page_path + '.zip'), f"Missing PDF zip file for {url}"
