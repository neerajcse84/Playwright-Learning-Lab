from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("http://127.0.0.1:5500/html/forms/11_file_upload_demo.html")

    page.get_by_label("Choose Resume").set_input_files(
        "sample_files/resume.pdf"
    )

    #page.get_by_role("button", name="Upload").click()

    expect(
        page.get_by_text("Uploaded: resume.pdf")
    ).to_be_visible()

    input("Press Enter to close...")

    browser.close()