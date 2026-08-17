from playwright.sync_api import sync_playwright,expect
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://127.0.0.1:5500/html/forms/06_checkbox_radio_demo.html")
    page.get_by_label("Python").check()
    page.get_by_label("Docker").uncheck()
    expect(page.get_by_label("Docker")).to_be_checked()
