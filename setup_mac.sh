echo "Setting up Selenium framework for Mac..."

# Check if Chrome is installed
if ! command -v "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" &> /dev/null; then
    echo "Google Chrome is not installed. Please install Chrome first."
    exit 1
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Clear webdriver cache
echo "Clearing webdriver cache..."
rm -rf ~/.wdm/

# Download ChromeDriver manually for ARM Macs
if [[ $(uname -m) == "arm64" ]]; then
    echo "Detected ARM-based Mac. Setting up ChromeDriver for ARM64..."

    # Get Chrome version
    CHROME_VERSION=$("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --version | awk '{print $3}')
    CHROME_MAJOR_VERSION=$(echo $CHROME_VERSION | cut -d'.' -f1)

    echo "Chrome version: $CHROME_VERSION"
    echo "Chrome major version: $CHROME_MAJOR_VERSION"

    # Create directory for chromedriver
    mkdir -p ~/chromedriver

    # Download the appropriate ChromeDriver
    echo "Downloading ChromeDriver for Chrome $CHROME_MAJOR_VERSION..."

    # You might need to update this URL based on the Chrome version
    CHROMEDRIVER_URL="https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_MAJOR_VERSION"
    CHROMEDRIVER_VERSION=$(curl -s $CHROMEDRIVER_URL)

    if [[ -z "$CHROMEDRIVER_VERSION" ]]; then
        echo "Could not determine ChromeDriver version. Using latest stable."
        CHROMEDRIVER_VERSION="114.0.5735.90"
    fi

    # Download ChromeDriver
    curl -o ~/chromedriver/chromedriver.zip "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_mac_arm64.zip"

    # Extract ChromeDriver
    cd ~/chromedriver
    unzip chromedriver.zip
    chmod +x chromedriver

    echo "ChromeDriver downloaded to ~/chromedriver"
    echo "You may need to add ~/chromedriver to your PATH"
fi

echo "Setup complete!"

