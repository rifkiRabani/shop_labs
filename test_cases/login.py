from playwright.sync_api import expect
import pytest
import allure

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
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
    
    
    