from playwright.sync_api import expect
import pytest
import allure

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from conftest import allure_metadata

@allure_metadata(
    title="Valid login with valid credentials.",
    description="this test case will validate user login with happy flow",
    feature="Login",
    testcase_url="https://shop.qaautomationlabs.com/",
    testcase_name="TC-01-001",
    suite="Login/",
    severity=allure.severity_level.CRITICAL,
)
def test_valid_login(page):
    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)
    page.goto("https://shop.qaautomationlabs.com/login")
    
    
    