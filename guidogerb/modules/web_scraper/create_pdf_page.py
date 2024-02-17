import pdfkit
import zipfile
import os

def create_pdf_page(url, pdf_page_path):
    # Convert HTML to PDF and save to the specified path
    try:
        pdfkit.from_url(url, pdf_page_path)
    except Exception as e:
        print(f"Error generating PDF for {url}: {e}")
        return

    # Zip the PDF file
    with zipfile.ZipFile(pdf_page_path + '.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(pdf_page_path, os.path.basename(pdf_page_path))

    # delete the original PDF file after zipping
    os.remove(pdf_page_path)

# Example usage
# create_pdf_page('http://example.com', '/path/to/output/example_com.page.pdf')
