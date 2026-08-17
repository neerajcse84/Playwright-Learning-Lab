from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    context = browser.new_context()

    page = context.new_page()

    page.goto("http://127.0.0.1:5500/html/basics/01_basic_page.html")

    expect(
        page.get_by_role("heading")
    ).to_have_text("Welcome to Playwright Learning Lab")

    print("✅ Assertion Passed")

    input("Press Enter to close the browser...")

    browser.close()