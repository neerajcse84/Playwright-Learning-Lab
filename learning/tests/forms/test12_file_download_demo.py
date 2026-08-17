from playwright.sync_api import sync_playwright
from pathlib import Path

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Open Application
    page.goto("http://127.0.0.1:5500/html/forms/12_file_download_demo.html")

    with page.expect_download() as download_info:
        page.get_by_role("button",name="Download Resume").click()

    download = download_info.value
    download.save_as("downloads/report.pdf")
    assert Path("downloads/report.pdf").exists()
    #print(download.suggested_filename)
    input("Press enter to close the browser....")
    browser.close()
