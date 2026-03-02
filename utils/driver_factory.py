"""
driver_factory.py

This module is responsible for:
- Creating WebDriver instances
- Supporting headless mode
- Future support for multiple browsers
- Centralizing driver configuration

Best Practice:
Never create driver directly inside test files.
Always use a factory pattern for scalability.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def get_driver(headless: bool = False) -> webdriver.Chrome:
    """
    Returns a configured Chrome WebDriver instance.

    :param headless: Run browser in headless mode if True
    """

    options = webdriver.ChromeOptions()

    # Global browser options
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")

    if headless:
        options.add_argument("--headless=new")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    return driver