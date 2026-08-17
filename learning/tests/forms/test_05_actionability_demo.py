from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    conext = browser.new_context()
    page = conext.new_page()
    page.goto("http://127.0.0.1:5500/html/forms/05_disabled_button_demo.html")
    
    page.get_by_role('button',name='Login').click()
    print(" Clicked Successfuly...")
    input("Press Enter to close....")
