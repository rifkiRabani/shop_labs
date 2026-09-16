from playwright.sync_api import sync_playwright
import pytest
import allure
BASE_URL = 'https://shop.qaautomationlabs.com/'


@pytest.fixture
def chrome():
    with sync_playwright() as p:
        with allure.step('Given user is in Login Page'):
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(BASE_URL)

        yield page
       
        with allure.step('Then User Close the browser'):
            ss = page.screenshot(path='test_evidence/imgs/test.png')
            allure.attach(ss, name='SS001', attachment_type=allure.attachment_type.PNG)
            browser.close()