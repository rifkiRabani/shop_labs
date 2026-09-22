import allure
from playwright.sync_api import Page
from playwright.sync_api import expect
from locators.login_loc import LoginLocators


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    def enter_email(self, email):
        with allure.step(f"Enter email: {email}"):
            self.page.get_by_test_id(LoginLocators.EMAIL_INPUT).fill(email)

    def enter_password(self, password):
        with allure.step(f"Enter password: {password}"):
            self.page.get_by_test_id(LoginLocators.PASSWORD_INPUT).fill(password)

    def check_remember_me(self):
        with allure.step("Check 'Remember Me' checkbox"):
            self.page.get_by_test_id(LoginLocators.CHECKBOX_REMEMBER_ME).check()

    def click_login_button(self):
        with allure.step("Click on the login button"):
            self.page.get_by_test_id(LoginLocators.LOGIN_BUTTON).click()
            self.page.wait_for_url("**/shop.php", timeout=15000)

    def login(self, email, password):
        with allure.step(f"Login with email: {email} and password: {password}"):
            self.enter_email(email)
            self.enter_password(password)
            self.check_remember_me()
            self.click_login_button()

    def get_invalid_email_error_message(self):
        with allure.step("Get invalid email error message"):
            return self.page.get_by_test_id(
                LoginLocators.INVALID_EMAIL_ERROR
            ).inner_text()

    def get_invalid_password_error_message(self):
        with allure.step("Get invalid password error message"):
            return self.page.get_by_test_id(
                LoginLocators.INVALID_EMAIL_OR_PASSWORD_ERROR
            ).inner_text()
