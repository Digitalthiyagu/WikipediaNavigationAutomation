"""
conftest.py

Purpose:
---------
Global Pytest configuration file.

Handles:
- Driver setup & teardown
- Safe screenshot capture on failure
- Edge-case crash prevention
- Proper pytest hook implementation

This version is defensive and production-safe.
"""

import pytest
from utils.driver_factory import get_driver
from utils.screenshot import take_screenshot


@pytest.fixture(scope="function")
def driver(request):
    """
    Creates WebDriver instance for each test.
    Ensures safe teardown and screenshot on failure.
    """

    driver = None

    try:
        # Create driver safely
        driver = get_driver(headless=False)

        yield driver

    except Exception as e:
        print(f"Driver setup error: {e}")
        raise

    finally:
        # Prevent edge-case crash if driver failed to initialize
        if driver:

            # Check if test actually executed and failed
            if hasattr(request.node, "rep_call"):
                if request.node.rep_call.failed:
                    try:
                        take_screenshot(driver, request.node.name)
                    except Exception as screenshot_error:
                        print(f"Screenshot capture failed: {screenshot_error}")

            # Always attempt to quit safely
            try:
                driver.quit()
            except Exception as quit_error:
                print(f"Driver quit failed: {quit_error}")


# ---------------------------------------------------------
# Safe Pytest Hook Implementation
# ---------------------------------------------------------

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Attaches test result object to item.
    Required for detecting failures in fixture.
    """

    outcome = yield
    rep = outcome.get_result()

    # Attach report to test item
    setattr(item, "rep_" + rep.when, rep)