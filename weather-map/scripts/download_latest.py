import os
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


def login_google(driver):
    """Log in to Google if a sign-in page appears."""
    email = os.getenv("GOOGLE_EMAIL")
    password = os.getenv("GOOGLE_PASSWORD")
    if not email or not password:
        raise RuntimeError(
            "GOOGLE_EMAIL and GOOGLE_PASSWORD environment variables must be set"
        )

    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
        )
    except TimeoutException:
        # Sign in page did not appear
        return

    driver.find_element(By.CSS_SELECTOR, "input[type='email']").send_keys(email)
    driver.find_element(By.ID, "identifierNext").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
    )
    driver.find_element(By.CSS_SELECTOR, "input[type='password']").send_keys(password)
    driver.find_element(By.ID, "passwordNext").click()

    WebDriverWait(driver, 15).until(EC.url_contains("weatherlab"))


def fetch_latest_csv():
    """Download the latest hurricane track CSV from DeepMind Weather Lab."""
    # Headless Chrome so the script can run without a GUI
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://deepmind.google.com/science/weatherlab")
        # Allow potential sign in page to load
        time.sleep(3)
        login_google(driver)
        # Allow the weather lab page to load after login
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
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    filename = f"FNV3_{today}.csv"
    response = requests.get(csv_url)
    response.raise_for_status()
    with open(os.path.join(data_dir, filename), "wb") as fh:
        fh.write(response.content)
    print(f"Downloaded {filename}")


if __name__ == "__main__":
    fetch_latest_csv()
