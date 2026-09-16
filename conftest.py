from playwright.sync_api import sync_playwright
import pytest
import allure
from pathlib import Path
BASE_URL = 'https://shop.qaautomationlabs.com/'


def allure_metadata(title, description, feature, testcase_url, testcase_name, suite, severity):
    def decorator(test_function):
        decorated_function = allure.title(title)(test_function)
        decorated_function = allure.description(description)(decorated_function)
        decorated_function = allure.feature(feature)(decorated_function)
        decorated_function = allure.testcase(testcase_url, name=testcase_name)(decorated_function)
        decorated_function = allure.suite(suite)(decorated_function)
        decorated_function = allure.severity(severity)(decorated_function)
        return decorated_function

    return decorator


@pytest.fixture
def chrome():
    with sync_playwright() as p:
        with allure.step('Given user is in Login Page'):
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(BASE_URL)

        yield page
       
        with allure.step('Then User Close the browser'):
            evidence_path = Path(__file__).parent / 'test_evidence' / 'imgs' / 'test.png'
            ss = page.screenshot(path=str(evidence_path))
            allure.attach(ss, name='SS001', attachment_type=allure.attachment_type.PNG)
            browser.close()