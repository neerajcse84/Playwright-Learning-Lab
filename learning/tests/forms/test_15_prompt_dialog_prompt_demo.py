from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Dialog callback
    def handle_dialog(dialog):
        print("Dialog type:", dialog.type)
        print("Dialog message:", dialog.message)

        # Enter value and click OK
        dialog.accept("Neeraj")

    # Register dialog listener
    page.on("dialog", handle_dialog)

    # Open application
    page.goto(
        "http://127.0.0.1:5500/html/forms/15_prompt_dialog_demo.html"
    )

    # Trigger prompt
    page.get_by_role("button", name="Enter Name").click()

    # Verify the result displayed by the page
    expect(page.locator("#result")).to_have_text("Hello Neeraj")

    print("Test Passed")

    input("Press Enter to close...")
    browser.close()