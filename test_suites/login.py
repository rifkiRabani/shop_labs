from playwright.sync_api import expect
import pytest
import allure

from shop_labs.pages.login.login_page import LoginPage
from shop_labs.pages.dashboard.dashboard_page import DashboardPage
from conftest import BASE_URL, allure_metadata


@allure_metadata(
    title="Valid login with valid credentials.",
    description="this test case will validate user login with happy flow",
    feature="Login",
    testcase_url="https://shop.qaautomationlabs.com/",
    testcase_name="TC-01-001",
    suite="Login",
    severity=allure.severity_level.CRITICAL,
)
def test_valid_login(chrome):
    login_page = LoginPage(chrome)
    dashboard_page = DashboardPage(chrome)
    chrome.goto(BASE_URL)
    loadstate = chrome.wait_for_load_state("networkidle", timeout=15000)
    login_page.login("demo@demo.com", "demo")
    dashboard_page.should_be_open()

def test_invalid_username(chrome):
    login_page = LoginPage(chrome)
    dashboard_page = DashboardPage(chrome)
    chrome.goto(BASE_URL)
    login_page.enter_email("invalid_username")
    login_page.enter_password("valid_password")
    login_page.check_remember_me()
    login_page.click_login_button()
    dashboard_page.should_not_be_open()