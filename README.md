# Selenium Python Scripts Framework

A comprehensive test automation framework using Selenium WebDriver, pytest, and Allure reporting with Docker and Jenkins integration.

## Features

- Page Object Model design pattern
- Cross-browser support (Chrome, Firefox, Edge)
- Allure reporting integration
- Configuration management
- Logging support
- Screenshot capture on failure
- Parallel test execution support
- Docker and Selenium Grid support
- Jenkins integration
- Easy to extend for different websites

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Local Usage

### Running Tests Locally

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_sample/test_login_saucedemo.py

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

## Docker and Selenium Grid

### Running Tests with Docker

The framework supports running tests in Docker containers with Selenium Grid for distributed test execution.

#### Prerequisites

- Docker and Docker Compose installed

#### Start Selenium Grid

```bash
docker-compose up -d selenium-hub chrome firefox edge
```

#### Run Tests with Docker

```bash
# Run all tests with default settings
./run_docker_tests.sh

# Run with specific browser and in headless mode
./run_docker_tests.sh -b firefox -h

# Run specific tests with markers in parallel
./run_docker_tests.sh -b chrome -p 4 -t tests/saucedemo -m smoke
```

#### Stop Selenium Grid

```bash
docker-compose down
```

## Jenkins Integration

This framework includes a Jenkinsfile for CI/CD integration. To set up in Jenkins:

1. Create a new Pipeline job in Jenkins
2. Configure it to use the Jenkinsfile from this repository
3. Set up necessary plugins:
   - Docker Pipeline
   - Allure Jenkins Plugin

Jenkins pipeline parameters:
- `BROWSER`: Browser to run tests (chrome, firefox, edge)
- `HEADLESS`: Run in headless mode (true/false)
- `TEST_PATH`: Path to tests
- `MARKERS`: Test markers (e.g., smoke)
- `PARALLEL_WORKERS`: Number of parallel workers

## Generating Allure Report

```bash
# Generate report
allure generate reports/allure-results -o reports/allure-report

# Open report
allure open reports/allure-report

# Generate and open report
allure serve reports/allure-results
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
- `docker-compose.yml`: Docker Compose configuration for Selenium Grid
- `Dockerfile`: Docker configuration for test runner
- `Jenkinsfile`: Jenkins pipeline configuration
- `run_docker_tests.sh`: Script to run tests in Docker