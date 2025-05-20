import time

import pytest
from selenium.webdriver.common.by import By
from base.base_page import BasePage
import allure


class HomePageSaucedemo(BasePage):
    """Sample home page for demonstration"""

    # Locators
    test1 = (By.XPATH, "//input[@id='user-name']")
    test2 = (By.XPATH, "//input[@id='password']")
    LOGIN_LINK = (By.XPATH, "//input[@id='login-button']")
    WELCOME_MESSAGE = (By.CLASS_NAME, "welcome-message")
    SEARCH_BOX = (By.ID, "search")
    SEARCH_BUTTON = (By.ID, "search-button")

    @allure.step("Navigate to login page")
    def go_to_login(self):
        """Click on login link"""
        self.click_element(self.LOGIN_LINK)

    @allure.step("Search for: {query}")
    def search(self, query):
        """Perform search"""
        self.enter_text(self.SEARCH_BOX, query)
        self.click_element(self.SEARCH_BUTTON)

    @allure.step("Get welcome message")
    def get_welcome_message(self):
        """Get welcome message text"""
        try:
            return self.get_text(self.WELCOME_MESSAGE)
        except:
            pytest.fail("Welcome message is not visible")
            return None