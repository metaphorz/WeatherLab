import os
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def fetch_latest_csv():
    """Download the latest hurricane track CSV from DeepMind Weather Lab."""
    # Headless Chrome so the script can run without a GUI
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://deepmind.google.com/science/weatherlab")
        # Allow dynamic content to load
        time.sleep(5)

        # Parse the page for a link ending with .csv
        soup = BeautifulSoup(driver.page_source, "html.parser")
        csv_url = None
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if href.endswith(".csv"):
                csv_url = href
                break
    finally:
        driver.quit()

    if not csv_url:
        raise RuntimeError("CSV download link not found.")

    # Save the file in the data directory with a timestamp-based name
    today = datetime.utcnow().strftime("%Y-%m-%d")
    os.makedirs("weather-map/data", exist_ok=True)
    filename = f"FNV3_{today}.csv"
    response = requests.get(csv_url)
    response.raise_for_status()
    with open(os.path.join("weather-map/data", filename), "wb") as fh:
        fh.write(response.content)
    print(f"Downloaded {filename}")


if __name__ == "__main__":
    fetch_latest_csv()
