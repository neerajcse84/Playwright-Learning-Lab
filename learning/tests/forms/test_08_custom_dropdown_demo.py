from playwright.sync_api import sync_playwright,expect
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    # Opening the URL
    page.goto("http://127.0.0.1:5500/html/forms/08_custom_dropdown_demo.html")
    page.locator("#dropdown").click()
    page.get_by_text("United Kingdom").click()
    expect(page.locator("#dropdown")).to_have_text("United Kingdom")
    