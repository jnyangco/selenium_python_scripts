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


class RemoteDriverFactory:
    """Factory class for creating local or remote WebDriver instances"""

    @staticmethod
    @allure.step("Creating driver: {browser_name} (Remote: {use_grid})")
    def create_driver(browser_name="chrome", headless=False, use_grid=False, hub_url=None):
        """Create and return WebDriver instance - local or remote"""
        logger = logging.getLogger(__name__)
        logger.info(f"Creating {browser_name} driver (Remote: {use_grid})")

        # Configure browser options based on browser type
        if browser_name.lower() == "chrome":
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")

        elif browser_name.lower() == "firefox":
            options = webdriver.FirefoxOptions()
            if headless:
                options.add_argument("--headless")

        elif browser_name.lower() == "edge":
            options = webdriver.EdgeOptions()
            if headless:
                options.add_argument("--headless")

        else:
            raise ValueError(f"Browser {browser_name} not supported")

        # Create driver - either remote or local
        if use_grid and hub_url:
            logger.info(f"Using Selenium Grid at {hub_url}")
            driver = webdriver.Remote(
                command_executor=hub_url,
                options=options
            )
        else:
            # Use local WebDriver
            logger.info("Using local WebDriver")
            if browser_name.lower() == "chrome":
                # Handle special case for ARM-based Macs
                system = platform.system()
                machine = platform.machine()

                if system == "Darwin" and machine == "arm64":
                    # For M1/M2 Macs
                    logger.info("Detected ARM-based Mac, configuring ChromeDriver accordingly")
                    chrome_driver_path = ChromeDriverManager().install()
                    driver_dir = os.path.dirname(chrome_driver_path)
                    chromedriver_path = None

                    for file in os.listdir(driver_dir):
                        if file == "chromedriver" or file.startswith("chromedriver"):
                            if not file.endswith(".txt") and not file.endswith(".md"):
                                chromedriver_path = os.path.join(driver_dir, file)
                                break

                    if chromedriver_path and os.path.exists(chromedriver_path):
                        os.chmod(chromedriver_path, 0o755)
                        service = ChromeService(chromedriver_path)
                    else:
                        service = ChromeService(ChromeDriverManager().install())
                else:
                    service = ChromeService(ChromeDriverManager().install())

                driver = webdriver.Chrome(service=service, options=options)

            elif browser_name.lower() == "firefox":
                driver = webdriver.Firefox(
                    service=FirefoxService(GeckoDriverManager().install()),
                    options=options
                )

            elif browser_name.lower() == "edge":
                driver = webdriver.Edge(
                    service=EdgeService(EdgeChromiumDriverManager().install()),
                    options=options
                )

        driver.maximize_window()
        logger.info(f"Driver created successfully")
        return driver