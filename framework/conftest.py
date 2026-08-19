import pytest
from playwright.sync_api import (
    sync_playwright,
    Browser,
    BrowserContext,
    Page
)
from framework.config import BASE_URL, BUILD_NUMBER
from framework.pages.login_page import LoginPage
from framework.pages.dashboard_page import DashboardPage
from framework.testdata.login_data import valid_admin_user
import pytest_html
from pathlib import Path
import base64
from pytest_metadata.plugin import metadata_key
import os




@pytest.fixture(scope="session")
def browser() -> Browser:

    with sync_playwright() as p:
        headless = os.getenv("HEADLESS", "true").lower() == "true"
        browser = p.chromium.launch(headless=headless)

        yield browser

        browser.close()

@pytest.fixture
def context(browser: Browser)-> BrowserContext:
    context = browser.new_context(base_url=BASE_URL)

    yield context

    context.close()

@pytest.fixture
def page(context: BrowserContext, request) -> Page:
    page = context.new_page()

    yield page

    page.close()


@pytest.fixture
def open_app(page):
    page.goto("/")
    return page

@pytest.fixture
def login_user(page):
    page.goto("/")
    login_page = LoginPage(page)
    user = valid_admin_user()
    login_page.login(user["username"],user["password"])
    yield page
    dashboard_page = DashboardPage(page)
    dashboard_page.logout()



@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    setattr(item, f"rep_{report.when}", report)

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")

        if page:
            screenshot_path = (
                Path("reports")
                / "screenshots"
                / f"{item.name}.png"
            ).resolve()

            # Save the actual PNG file
            page.screenshot(path=str(screenshot_path))

            # Read PNG and convert it to base64 text
            image_data = base64.b64encode(
                screenshot_path.read_bytes()
            ).decode("utf-8")

            # Embed the image directly into HTML
            html = f"""
                <div>
                    <h4>Failure Screenshot</h4>
                    <img
                        src="data:image/png;base64,{image_data}"
                        alt="Failure Screenshot"
                        style="max-width: 100%;"
                        onclick="window.open(this.src)"
                    />
                </div>
            """

            extras = getattr(report, "extras", [])
            extras.append(
                pytest_html.extras.html(html)
            )

            report.extras = extras

def pytest_configure(config):
    config.stash[metadata_key]["Base URL"] = BASE_URL