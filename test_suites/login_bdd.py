from pytest_bdd import given, scenarios, then, when, parsers

from shop_labs.conftest import BASE_URL
from shop_labs.pages.dashboard.dashboard_page import DashboardPage
from shop_labs.pages.login.login_page import LoginPage


scenarios("../features/login/login.feature")


@given("the user is on the login page")
def user_is_on_login_page(chrome):
    chrome.goto(BASE_URL)


@when(
    parsers.parse(
        'the user logs in with email "{email}" and password "{password}"'
    )
)
def user_logs_in(chrome, email, password):
    LoginPage(chrome).login(email, password)


@when(
    parsers.parse(
        'the user submits username "{username}" and password "{password}"'
    )
)
def user_submits_invalid_login(chrome, username, password):
    login_page = LoginPage(chrome)
    login_page.enter_email(username)
    login_page.enter_password(password)
    login_page.check_remember_me()
    login_page.click_login_button()


@then("the dashboard should be open")
def dashboard_should_be_open(chrome):
    DashboardPage(chrome).should_be_open()


@then("the dashboard should not be open")
def dashboard_should_not_be_open(chrome):
    DashboardPage(chrome).should_not_be_open()
