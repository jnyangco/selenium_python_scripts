# selenium_python_scripts

```markdown
# Selenium Page Object Model Framework

A comprehensive test automation framework using Selenium WebDriver, pytest, and Allure reporting.

## Features

- Page Object Model design pattern
- Cross-browser support (Chrome, Firefox, Edge)
- Allure reporting integration
- Configuration management
- Logging support
- Screenshot capture on failure
- Parallel test execution support
- Easy to extend for different websites

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_sample/test_saucedemo_login.py

# Run tests with specific marker
pytest -m smoke

# Run tests in parallel
pytest -n 4

# Run tests with specific browser
BROWSER=firefox pytest
```

### Configuration

Set environment variables or modify `config/config.py`:

- `BROWSER`: Browser to use (chrome, firefox, edge)
- `HEADLESS`: Run in headless mode (true/false)
- `BASE_URL`: Base URL for tests

### Generating Allure Report

```bash
# 1.1 Generate report
allure generate reports/allure-results -o reports/allure-report

# 1.2 Open report
allure open reports/allure-report

# 2.1 Generate and open report
allure serve reports/allure-result
```

## Adding New Tests

1. Create page objects in `pages/` directory
2. Create test files in `tests/` directory
3. Use the base classes provided for consistent behavior

## Project Structure

- `base/`: Base classes and utilities
- `pages/`: Page object classes
- `tests/`: Test cases
- `config/`: Configuration files
- `utils/`: Utility functions
- `reports/`: Test reports and screenshots

## Example Test

```python
import pytest
from pages.saucedemo.saucedemo_login_page import SaucedemoLoginPage


class TestLogin:
    def test_valid_login(self, driver, config):
        login_page = SaucedemoLoginPage(driver)
        login_page.open_url(config.BASE_URL)
        login_page.login("user", "password")
        assert SaucedemoLoginPage.is_logged_in()
```
```