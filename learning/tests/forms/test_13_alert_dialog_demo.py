from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    def handle_dialog(dialog):
        print(dialog.type)      # alert
        print(dialog.message)   # Welcome Neeraj!
        dialog.accept()

    page.on("dialog", handle_dialog)

    page.goto("http://127.0.0.1:5500/html/forms/13_alert_dialog_demo.html")

    page.get_by_role("button", name="Show Alert").click()

    input("Press Enter to close...")
    browser.close()