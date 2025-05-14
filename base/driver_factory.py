import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import logging
import platform
import os


class DriverFactory:
    """Factory class for creating WebDriver instances"""

    @staticmethod
    @allure.step("Creating {browser_name} driver")
    def create_driver(browser_name="chrome", headless=False):
        """Create and return WebDriver instance"""
        logger = logging.getLogger(__name__)
        logger.info(f"Creating {browser_name} driver")

        if browser_name.lower() == "chrome":
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")

            # Fix for ARM-based Macs
            system = platform.system()
            machine = platform.machine()

            if system == "Darwin" and machine == "arm64":
                # For M1/M2 Macs
                logger.info("Detected ARM-based Mac, configuring ChromeDriver accordingly")
                chrome_driver_path = ChromeDriverManager().install()

                # Find the actual chromedriver executable
                driver_dir = os.path.dirname(chrome_driver_path)
                chromedriver_path = None

                for file in os.listdir(driver_dir):
                    if file == "chromedriver" or file.startswith("chromedriver"):
                        if not file.endswith(".txt") and not file.endswith(".md"):
                            chromedriver_path = os.path.join(driver_dir, file)
                            break

                if not chromedriver_path:
                    # Fallback: try to find chromedriver in common locations
                    possible_paths = [
                        os.path.join(driver_dir, "chromedriver"),
                        os.path.join(driver_dir, "chromedriver-mac-arm64"),
                        os.path.join(driver_dir, "chromedriver-mac-x64"),
                    ]

                    for path in possible_paths:
                        if os.path.exists(path) and os.path.isfile(path):
                            chromedriver_path = path
                            break

                if chromedriver_path and os.path.exists(chromedriver_path):
                    # Make sure it's executable
                    os.chmod(chromedriver_path, 0o755)
                    service = ChromeService(chromedriver_path)
                else:
                    # Fallback to default installation
                    service = ChromeService(ChromeDriverManager().install())
            else:
                # For other systems, use default installation
                service = ChromeService(ChromeDriverManager().install())

            driver = webdriver.Chrome(service=service, options=options)

        elif browser_name.lower() == "firefox":
            options = webdriver.FirefoxOptions()
            if headless:
                options.add_argument("--headless")

            driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()),
                options=options
            )

        elif browser_name.lower() == "edge":
            options = webdriver.EdgeOptions()
            if headless:
                options.add_argument("--headless")

            driver = webdriver.Edge(
                service=EdgeService(EdgeChromiumDriverManager().install()),
                options=options
            )

        else:
            raise ValueError(f"Browser {browser_name} not supported")

        driver.maximize_window()
        logger.info(f"{browser_name} driver created successfully")
        return driver