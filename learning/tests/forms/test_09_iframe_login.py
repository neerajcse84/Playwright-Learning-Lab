from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    context = browser.new_context()

    page = context.new_page()

    page.goto("http://127.0.0.1:5500/html/forms/09_iframe_demo.html")

    login_frame = page.frame_locator("#loginFrame")

    username = login_frame.locator("#username")
    password = login_frame.locator("#password")

    username.fill("Neeraj")
    password.fill("Neeraj@234")

    expect(username).to_have_value("Neeraj")

    input("Press Enter to close...")

    browser.close()