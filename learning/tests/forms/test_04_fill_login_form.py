from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://127.0.0.1:5500/html/forms/04_login_page.html")
    page.get_by_label("Username").fill("neeraj tripathi")
    page.get_by_label("Password").fill("neeraj@1234")
    page.get_by_label("Remember Me").check()
    page.get_by_label("Remember Me").check()
    page.get_by_label("Remember Me").uncheck()
    page.get_by_label("Remember Me").click()
    page.get_by_label("Remember Me").click()
    page.get_by_label("Remember Me").check()
    print(page.get_by_label("Remember Me").is_checked())



    input("Press Enter to close..")
    browser.close()

