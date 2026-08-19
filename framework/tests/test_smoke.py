import os
import pytest
from playwright.sync_api import Page


@pytest.mark.deployment_smoke
def test_application_smoke(page: Page):
    app_url = os.getenv(
        "APP_URL",
        "http://127.0.0.1:5000"
    )

    page.goto(app_url)

    assert page.get_by_role(
        "heading",
        name="Employee Management System"
    ).is_visible()