from framework.pages.login_page import LoginPage
from framework.pages.dashboard_page import DashboardPage
from framework.config import BASE_URL
import pytest
from framework.testdata.login_data import INVALID_LOGIN_DATA
from framework.testdata.login_data import valid_admin_user
from framework.testdata.login_data import invalid_password_user

@pytest.mark.parametrize(
    "test_data, expected_result",
    INVALID_LOGIN_DATA
)
def test_invalid_login(page, test_data, expected_result):

    login_page = LoginPage(page)

    page.goto("/")

    assert page.get_by_role(
        "heading",
        name="Employee Management System"
    ).is_visible()

    login_page.login(
        test_data["username"],
        test_data["password"]
    )

    assert page.get_by_text(
        expected_result
    ).is_visible()

@pytest.mark.smoke
def test_valid_login(page):

    user = valid_admin_user()
    login_page = LoginPage(page)
    
    page.goto("/")

    assert page.get_by_role(
        "heading",
        name="Employee Management System"
        ).is_visible()

    login_page.login(user["username"],user["password"])

    assert page.get_by_role(
                "heading",
                name="Dashboard"
            ).is_visible()


@pytest.mark.smoke
@pytest.mark.regression
def test_logout(page):
    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)

    page.goto("/")
    
    assert page.get_by_role(
            "heading",
            name="Employee Management System"
            ).is_visible()
    
    login_page.login("admin", "admin123")
    assert page.get_by_role(
                    "heading",
                    name="Dashboard"
                ).is_visible()
    dashboard_page.logout()
    assert page.get_by_role("heading",name="Login").is_visible()
    page.goto("/dashboard")

    assert page.get_by_role(
    "heading",
    name="Login"
).is_visible()

def test_home_page(open_app):
    assert open_app.get_by_role(
    "heading",
    name="Employee Management System"
)

def test_dashboard_with_login(login_user):
    assert login_user.get_by_role(
        "heading",
        name="Dashboard"
    ).is_visible()

def test_invalid_password_scenario(page):
    user = invalid_password_user()

    login_page = LoginPage(page)

    page.goto("/")

    login_page.login(
        user["username"],
        user["password"]
    )

    assert page.get_by_text("Invalid credentials").is_visible()



    