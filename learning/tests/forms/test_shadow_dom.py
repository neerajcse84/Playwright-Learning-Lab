from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("http://127.0.0.1:5500/html/forms/shadow_dom.html")

    username = page.get_by_placeholder("Username")
    username.fill("Neeraj")

    password = page.get_by_placeholder("Password")
    password.fill("Playwright")

    page.get_by_role("button", name="Login").click()

    print(page.get_by_text("Login successful").text_content())

    browser.close()