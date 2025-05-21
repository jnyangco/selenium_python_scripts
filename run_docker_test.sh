#!/usr/bin/env bash
set -e

# Default values
BROWSER=${BROWSER:-"chrome"}
HEADLESS=${HEADLESS:-"false"}
PARALLEL=${PARALLEL:-"2"}
TEST_PATH=${TEST_PATH:-"tests"}
MARKERS=${MARKERS:-""}

# Help function
function show_help {
    echo "Usage: ./run_docker_tests.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -b, --browser BROWSER    Browser to use (chrome, firefox, edge)"
    echo "  -h, --headless           Run in headless mode"
    echo "  -p, --parallel WORKERS   Number of parallel workers"
    echo "  -t, --tests PATH         Path to test files/directories"
    echo "  -m, --markers MARKERS    Run tests with specific markers"
    echo "  --help                   Show this help message"
    echo ""
    echo "Example:"
    echo "  ./run_docker_tests.sh -b firefox -h -p 4 -t tests/saucedemo -m smoke"
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -b|--browser)
            BROWSER="$2"
            shift 2
            ;;
        -h|--headless)
            HEADLESS="true"
            shift
            ;;
        -p|--parallel)
            PARALLEL="$2"
            shift 2
            ;;
        -t|--tests)
            TEST_PATH="$2"
            shift 2
            ;;
        -m|--markers)
            MARKERS="$2"
            shift 2
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Build marker argument
MARKER_ARG=""
if [ ! -z "$MARKERS" ]; then
    MARKER_ARG="-m $MARKERS"
fi

# Start Selenium Grid
echo "Starting Selenium Grid..."
docker-compose up -d selenium-hub chrome firefox edge

# Wait for Grid to be ready
echo "Waiting for Selenium Grid to be ready..."
sleep 10

# Build test runner image if necessary
docker-compose build test-runner

# Run tests
echo "Running tests with browser: $BROWSER, headless: $HEADLESS, parallel workers: $PARALLEL"
docker-compose run \
    -e BROWSER=$BROWSER \
    -e HEADLESS=$HEADLESS \
    -e USE_GRID=true \
    -e PARALLEL_WORKERS=$PARALLEL \
    test-runner \
    pytest $TEST_PATH -v -n $PARALLEL $MARKER_ARG

# Cleanup
read -p "Do you want to stop the Selenium Grid containers? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Stopping Selenium Grid..."
    docker-compose down
else
    echo "Selenium Grid is still running. Use 'docker-compose down' to stop it."
fi