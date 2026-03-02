"""
wikipedia_page.py

Improved robust version:
Handles both direct redirect and search result page.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class WikipediaPage:

    SEARCH_BOX = (By.NAME, "search")
    FIRST_RESULT = (By.CSS_SELECTOR, "ul.mw-search-results li a")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def open_homepage(self):
        self.driver.get("https://www.wikipedia.org/")

    def search(self, text: str):
        search_input = self.wait.until(
            EC.visibility_of_element_located(self.SEARCH_BOX)
        )
        search_input.clear()
        search_input.send_keys(text)
        search_input.send_keys(Keys.RETURN)

    def click_first_result_if_present(self):
        """
        Click first search result only if results page appears.
        If direct article loads, skip clicking.
        """
        try:
            first_result = self.wait.until(
                EC.element_to_be_clickable(self.FIRST_RESULT)
            )
            first_result.click()
        except TimeoutException:
            # Direct article page loaded — no need to click
            pass

    def wait_for_title_contains(self, text: str):
        self.wait.until(EC.title_contains(text))

    def get_page_title(self) -> str:
        return self.driver.title