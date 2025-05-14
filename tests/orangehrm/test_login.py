import time

import pytest
import allure
from pages.saucedemo.login_page import LoginPage
from pages.saucedemo.home_page import HomePage


@allure.feature("Login")
@allure.story("User Authentication")
class TestLogin:
    """Test suite for login functionality"""

    @allure.title("Valid Login Test")
    @allure.description("Test login with valid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_valid_login(self, driver, config):
        """Test login with valid credentials"""
        # Navigate to home page
        home_page = HomePage(driver)
        home_page.open_url(config.BASE_URL)

        # Go to login page
        home_page.go_to_login()
        time.sleep(10);

        # Perform login
        # login_page = LoginPage(driver)
        # login_page.login("testuser", "password123")

        # Verify successful login
        # assert "Welcome" in home_page.get_welcome_message()

    # @allure.title("Invalid Login Test")
    # @allure.description("Test login with invalid credentials")
    # @allure.severity(allure.severity_level.NORMAL)
    # def test_invalid_login(self, driver, config):
    #     """Test login with invalid credentials"""
    #     # Navigate to login page
    #     login_page = LoginPage(driver)
    #     login_page.open_url(f"{config.BASE_URL}/login")
    #
    #     # Perform login with invalid credentials
    #     login_page.login("invalid_user", "wrong_password")
    #
    #     # Verify error message
    #     assert login_page.is_error_displayed()
    #     assert "Invalid credentials" in login_page.get_error_message()