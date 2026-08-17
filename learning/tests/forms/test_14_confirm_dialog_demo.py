from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Callback function - executed automatically when a dialog appears
    def handle_dialog(dialog):
        print(f"Dialog Type    : {dialog.type}")
        print(f"Dialog Message : {dialog.message}")

        # Click OK
        dialog.accept()

        # For Cancel, use:
        # dialog.dismiss()

    # Register the event listener
    page.on("dialog", handle_dialog)

    # Open the page
    page.goto("http://127.0.0.1:5500/html/forms/14_confirm_dialog_demo.html")

    # Trigger the confirm dialog
    page.get_by_role("button", name="Delete Record").click()

    # Verify the result after clicking OK
    expect(page.locator("#result")).to_have_text("Record Deleted")

    print("✅ Test Passed")

    input("Press Enter to close the browser...")
    browser.close()