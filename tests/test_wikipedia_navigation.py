"""
test_wikipedia_navigation.py

Enterprise-Grade Test Layer

Principles:
-----------
- No browser setup logic
- No locators here
- No hardcoded assumptions
- Clean assertions
- Parameterized for scalability
- Logging included
- Easy to extend for data-driven testing
"""

import pytest
from pages.wikipedia_page import WikipediaPage
from utils.logger import get_logger

logger = get_logger(__name__)


# ----------------------------------------------------------------------
# Test Data (Can later move to JSON/CSV/Config file)
# ----------------------------------------------------------------------

TEST_DATA = [
    ("Selenium (software)", "Selenium"),
]


# ----------------------------------------------------------------------
# Test Case
# ----------------------------------------------------------------------

@pytest.mark.smoke
@pytest.mark.parametrize("search_term, expected_title", TEST_DATA)
def test_wikipedia_search_navigation(driver, search_term, expected_title):
    """
    Test Scenario:
    1. Open Wikipedia homepage
    2. Search for given term
    3. Handle dynamic navigation (result page or direct redirect)
    4. Validate that page title contains expected text

    This test is:
    - Data-driven
    - Modular
    - Reusable
    - CI/CD friendly
    """

    logger.info("===== TEST STARTED =====")
    logger.info(f"Search Term: {search_term}")

    wiki = WikipediaPage(driver)

    # Step 1: Open homepage
    wiki.open_homepage()

    # Step 2: Perform search
    wiki.search(search_term)

    # Step 3: Handle dynamic navigation safely
    wiki.click_first_result_if_present()

    # Step 4: Wait for title validation
    wiki.wait_for_title_contains(expected_title)

    actual_title = wiki.get_page_title()

    logger.info(f"Page title after navigation: {actual_title}")

    # Assertion with clear error message
    assert expected_title in actual_title, (
        f"Expected '{expected_title}' to be in page title, "
        f"but got '{actual_title}'"
    )

    logger.info("===== TEST PASSED SUCCESSFULLY =====")