from selenium.webdriver.common.by import By
from base.base_page import BasePage
import allure


class LoginPageSaucedemo(BasePage):
    """Sample login page for demonstration"""

    # Locators
    USERNAME_INPUT = (By.XPATH, "//input[@id='user-name']")
    PASSWORD_INPUT = (By.XPATH, "//input[@id='password']")
    LOGIN_BUTTON = (By.XPATH, "//input[@id='login-button']")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")

    @allure.step("Login with username: {username} and password: {password}")
    def login(self, username, password):
        """Perform login action"""
        self.enter_text(self.USERNAME_INPUT, username)
        self.enter_text(self.PASSWORD_INPUT, password)
        self.click_element(self.LOGIN_BUTTON)

    @allure.step("Check if error message is displayed")
    def is_error_displayed(self):
        """Check if error message is displayed"""
        return self.is_element_displayed(self.ERROR_MESSAGE)

    @allure.step("Get error message text")
    def get_error_message(self):
        """Get error message text"""
        return self.get_text(self.ERROR_MESSAGE)