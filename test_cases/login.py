from playwright.sync_api import expect
import pytest
import allure

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

@allure.title("Valid login with valid credentials.")
@allure.description("this test case will validate user login with happy flow")
@allure.feature("Login")
@allure.testcase("https://shop.qaautomationlabs.com/", name="TC-01-001")
@allure.suite("Login/")
@allure.severity(allure.severity_level.CRITICAL)
def test_valid_login(page):
    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)
    page.goto("https://shop.qaautomationlabs.com/login")
    