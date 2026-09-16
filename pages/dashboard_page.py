import allure
from playwright.sync_api import Page, expect

from locators.dashboard_loc import DashboardLocators

class DashboardPage:
    def __init__(self, page: Page):
        self.page = page

    def should_be_open(self):
        with allure.step("Validate dashboard page is open"):
            expect(self.page).to_have_url(DashboardLocators.PAGE_URL)
