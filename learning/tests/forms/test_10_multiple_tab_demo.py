from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    # Launch browser
    browser = p.chromium.launch(headless=False)

    # Create browser context
    context = browser.new_context()

    # Open main page
    page = context.new_page()

    page.goto("http://127.0.0.1:5500/html/forms/10_multiple_tabs_demo.html")

    # Wait for a new tab while clicking the button
    with context.expect_page() as new_page_info:
        page.get_by_role("button", name="Open Report").click()

    # Capture the newly opened tab
    report_page = new_page_info.value

    # Wait until the new page is fully loaded
    report_page.wait_for_load_state()

    # Verify report page
    expect(report_page).to_have_title("Report")
    expect(
        report_page.get_by_role("heading", name="Monthly Report")
    ).to_have_text("Monthly Report")

    # Close the report tab
    report_page.close()

    # Verify we are still on the main page
    expect(page).to_have_title("Multiple Tabs Demo")

    input("Press Enter to close the browser...")

    browser.close()