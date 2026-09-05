import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def create_chrome_driver(headless: bool = True) -> webdriver.Chrome:
    """Create a Chrome WebDriver.

    Locally, Selenium Manager downloads the matching chromedriver automatically.
    In Docker/production, CHROME_BIN and CHROMEDRIVER_PATH point at the system
    Chromium and its driver so nothing has to be downloaded at runtime.
    """
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    chrome_bin = os.getenv("CHROME_BIN")
    if chrome_bin:
        options.binary_location = chrome_bin

    driver_path = os.getenv("CHROMEDRIVER_PATH")
    if driver_path:
        driver = webdriver.Chrome(service=Service(driver_path), options=options)
    else:
        driver = webdriver.Chrome(options=options)

    driver.set_page_load_timeout(30)
    return driver
