import os
from dataclasses import dataclass


@dataclass
class TestConfig:
    """Test configuration"""
    # Browser settings
    BROWSER: str = os.getenv("BROWSER", "chrome")
    HEADLESS: bool = os.getenv("HEADLESS", "False").lower() == "true"

    # Test settings
    BASE_URL: str = os.getenv("BASE_URL", "https://www.saucedemo.com/")
    IMPLICIT_WAIT: int = int(os.getenv("IMPLICIT_WAIT", "10"))
    EXPLICIT_WAIT: int = int(os.getenv("EXPLICIT_WAIT", "10"))

    # Report settings
    SCREENSHOTS_DIR: str = os.getenv("SCREENSHOTS_DIR", "reports/screenshots")
    ALLURE_RESULTS_DIR: str = os.getenv("ALLURE_RESULTS_DIR", "reports/allure-results")

    # Logging settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "reports/test.log")