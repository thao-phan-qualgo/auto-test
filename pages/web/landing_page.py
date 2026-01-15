"""Landing page object."""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LandingPage(BasePage):
    """Landing page object."""

    # Page locators
    PAGE_TITLE = (By.TAG_NAME, "title")

    def navigate_to_landing_page(self, base_url: str) -> "LandingPage":
        """Navigate to landing page."""
        url = base_url.rstrip("/")
        self.open(url)
        self.wait_for_page_load()
        return self

    def get_page_title(self) -> str:
        """Get page title."""
        return self.title

    def is_on_home_page(self, base_url: str) -> bool:
        """Check if currently on home page."""
        expected = base_url.rstrip("/")
        current = self.current_url.rstrip("/")
        return current == expected or current == f"{expected}/"
