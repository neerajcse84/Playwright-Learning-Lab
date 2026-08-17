from playwright.sync_api import sync_playwright,expect
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://127.0.0.1:5500/html/forms/07_dropdown_demo.html")
    page.get_by_label("Choose Country").select_option(value='india')
    expect(page.get_by_label("Choose Country")).to_have_value("india")
    expect(page.get_by_label("Choose Country")).to_contain_text("India")
    expect(page.get_by_label("Choose Country")).not_to_contain_text("United Kingdom")
    input("Press Enter to close the browser")
    browser.close()