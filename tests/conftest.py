import pytest
import allure
from base.driver_factory import DriverFactory
from config.config import TestConfig
from utils.logger import setup_logger
from utils.screenshot_utils import ScreenshotUtils


# Setup logger
logger = setup_logger()

@pytest.fixture(scope="function")
def driver():
    """Create and yield WebDriver instance"""
    config = TestConfig()

    # Create driver
    driver = DriverFactory.create_driver(
        browser_name=config.BROWSER,
        headless=config.HEADLESS
    )

    # Set implicit wait
    driver.implicitly_wait(config.IMPLICIT_WAIT)

    yield driver

    # Take screenshot on failure
    if hasattr(pytest, "_test_failed") and pytest._test_failed:
        screenshot_util = ScreenshotUtils(driver)
        screenshot_util.take_screenshot("test_failure")

    # Quit driver
    driver.quit()


@pytest.fixture(scope="function")
def config():
    """Return test configuration"""
    return TestConfig()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to add screenshot on test failure"""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        pytest._test_failed = True
    else:
        pytest._test_failed = False