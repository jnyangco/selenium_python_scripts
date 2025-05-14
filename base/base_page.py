import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
from utils.screenshot_utils import ScreenshotUtils


class BasePage:
    """Base class for all page objects"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.screenshot_util = ScreenshotUtils(driver)

    @allure.step("Opening URL: {url}")
    def open_url(self, url):
        """Navigate to specified URL"""
        self.logger.info(f"Opening URL: {url}")
        self.driver.get(url)

    @allure.step("Finding element: {locator}")
    def find_element(self, locator, timeout=10):
        """Find element with explicit wait"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            self.logger.info(f"Found element: {locator}")
            return element
        except TimeoutException:
            self.logger.error(f"Element not found: {locator}")
            self.screenshot_util.take_screenshot("element_not_found")
            raise

    @allure.step("Finding elements: {locator}")
    def find_elements(self, locator, timeout=10):
        """Find multiple elements with explicit wait"""
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
            self.logger.info(f"Found {len(elements)} elements: {locator}")
            return elements
        except TimeoutException:
            self.logger.error(f"Elements not found: {locator}")
            self.screenshot_util.take_screenshot("elements_not_found")
            return []

    @allure.step("Clicking element: {locator}")
    def click(self, locator):
        """Click an element"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.logger.info(f"Clicking element: {locator}")
        element.click()

    @allure.step("Typing text: {text} into element: {locator}")
    def send_keys(self, locator, text):
        """Send keys to an element"""
        element = self.find_element(locator)
        element.clear()
        self.logger.info(f"Typing: {text} into element: {locator}")
        element.send_keys(text)

    @allure.step("Getting text from element: {locator}")
    def get_text(self, locator):
        """Get text from an element"""
        element = self.find_element(locator)
        text = element.text
        self.logger.info(f"Got text: {text} from element: {locator}")
        return text

    @allure.step("Checking if element is displayed: {locator}")
    def is_displayed(self, locator):
        """Check if element is displayed"""
        try:
            element = self.find_element(locator)
            is_displayed = element.is_displayed()
            self.logger.info(f"Element {locator} is {'displayed' if is_displayed else 'not displayed'}")
            return is_displayed
        except (TimeoutException, NoSuchElementException):
            self.logger.info(f"Element {locator} is not displayed")
            return False

    @allure.step("Waiting for element to be visible: {locator}")
    def wait_for_element_visible(self, locator, timeout=10):
        """Wait for element to be visible"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            self.logger.info(f"Element is visible: {locator}")
            return element
        except TimeoutException:
            self.logger.error(f"Element not visible: {locator}")
            self.screenshot_util.take_screenshot("element_not_visible")
            raise

    @allure.step("Hovering over element: {locator}")
    def hover(self, locator):
        """Hover over an element"""
        element = self.find_element(locator)
        ActionChains(self.driver).move_to_element(element).perform()
        self.logger.info(f"Hovered over element: {locator}")

    @allure.step("Scrolling to element: {locator}")
    def scroll_to_element(self, locator):
        """Scroll to element"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        self.logger.info(f"Scrolled to element: {locator}")

    @allure.step("Getting page title")
    def get_title(self):
        """Get page title"""
        title = self.driver.title
        self.logger.info(f"Page title: {title}")
        return title