import os
import platform
import subprocess
from webdriver_manager.chrome import ChromeDriverManager


def fix_chromedriver():
    """Fix ChromeDriver issues on Mac"""
    system = platform.system()
    machine = platform.machine()

    if system == "Darwin":
        print(f"Detected {system} {machine}")

        # Clear webdriver cache
        cache_dir = os.path.expanduser("~/.wdm")
        if os.path.exists(cache_dir):
            print(f"Clearing cache directory: {cache_dir}")
            subprocess.run(["rm", "-rf", cache_dir])

        # Download fresh ChromeDriver
        print("Downloading fresh ChromeDriver...")
        driver_path = ChromeDriverManager().install()
        print(f"ChromeDriver installed at: {driver_path}")

        # Make sure it's executable
        driver_dir = os.path.dirname(driver_path)
        for file in os.listdir(driver_dir):
            if file.startswith("chromedriver") and not file.endswith(".txt"):
                full_path = os.path.join(driver_dir, file)
                os.chmod(full_path, 0o755)
                print(f"Made executable: {full_path}")


if __name__ == "__main__":
    fix_chromedriver()