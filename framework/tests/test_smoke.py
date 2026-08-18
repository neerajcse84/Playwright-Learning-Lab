from playwright.sync_api import Page


def test_application_smoke(page: Page):
    page.goto("http://127.0.0.1:5001")

    assert page.get_by_role(
        "heading",
        name="Employee Management System"
    ).is_visible()