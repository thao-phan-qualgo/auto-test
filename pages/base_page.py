"""Base page class for Page Object Model."""

from typing import Tuple, Optional
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from core.config import settings
from core.logger import logger


class BasePage:
    """Base page class with common WebDriver operations."""

    def __init__(self, driver: WebDriver):
        """Initialize base page with WebDriver instance."""
        self.driver = driver
        self.wait = WebDriverWait(driver, settings.explicit_wait)

    def open(self, url: str) -> "BasePage":
        """Navigate to URL."""
        logger.info(f"Navigating to: {url}")
        self.driver.get(url)
        return self

    @property
    def current_url(self) -> str:
        """Get current page URL."""
        return self.driver.current_url

    @property
    def title(self) -> str:
        """Get page title."""
        return self.driver.title

    def find_element(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> WebElement:
        """Find element by locator."""
        wait = WebDriverWait(self.driver, timeout or settings.explicit_wait)
        return wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> list[WebElement]:
        """Find multiple elements by locator."""
        wait = WebDriverWait(self.driver, timeout or settings.explicit_wait)
        wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)

    def click(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> "BasePage":
        """Click element."""
        element = self.wait_for_clickable(locator, timeout)
        logger.debug(f"Clicking element: {locator}")
        element.click()
        return self

    def type(self, locator: Tuple[str, str], text: str, timeout: Optional[int] = None) -> "BasePage":
        """Type text into input field."""
        element = self.wait_for_clickable(locator, timeout)
        logger.debug(f"Typing '{text}' into element: {locator}")
        element.clear()
        element.send_keys(text)
        return self

    def get_text(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> str:
        """Get text from element."""
        element = self.find_element(locator, timeout)
        return element.text

    def is_displayed(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> bool:
        """Check if element is displayed."""
        try:
            wait = WebDriverWait(self.driver, timeout or 5)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def is_enabled(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> bool:
        """Check if element is enabled."""
        try:
            element = self.find_element(locator, timeout)
            return element.is_enabled()
        except (TimeoutException, NoSuchElementException):
            return False

    def wait_for_clickable(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> WebElement:
        """Wait for element to be clickable."""
        wait = WebDriverWait(self.driver, timeout or settings.explicit_wait)
        return wait.until(EC.element_to_be_clickable(locator))

    def wait_for_visible(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> WebElement:
        """Wait for element to be visible."""
        wait = WebDriverWait(self.driver, timeout or settings.explicit_wait)
        return wait.until(EC.visibility_of_element_located(locator))

    def wait_for_page_load(self, timeout: Optional[int] = None) -> "BasePage":
        """Wait for page to load completely."""
        wait = WebDriverWait(self.driver, timeout or settings.explicit_wait)
        wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        return self

    def scroll_to_element(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> "BasePage":
        """Scroll to element."""
        element = self.find_element(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        return self

    def take_screenshot(self, filename: str) -> "BasePage":
        """Take screenshot."""
        self.driver.save_screenshot(filename)
        logger.info(f"Screenshot saved: {filename}")
        return self
