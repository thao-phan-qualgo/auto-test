"""WebDriver factory for creating browser instances."""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from core.config import settings
from core.logger import logger


class WebDriverFactory:
    """Factory for creating WebDriver instances."""

    @staticmethod
    def create_driver() -> webdriver.Remote:
        """Create and configure WebDriver instance."""
        browser = settings.browser.lower()

        if browser == "chrome":
            return WebDriverFactory._create_chrome_driver()
        elif browser == "firefox":
            return WebDriverFactory._create_firefox_driver()
        elif browser == "edge":
            return WebDriverFactory._create_edge_driver()
        else:
            raise ValueError(f"Unsupported browser: {browser}")

    @staticmethod
    def _create_chrome_driver() -> webdriver.Chrome:
        """Create Chrome WebDriver using Selenium's built-in driver manager."""
        options = ChromeOptions()
        if settings.headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        # Selenium 4.6+ has built-in driver manager
        driver = webdriver.Chrome(options=options)
        WebDriverFactory._configure_driver(driver)
        logger.info("Chrome WebDriver created")
        return driver

    @staticmethod
    def _create_firefox_driver() -> webdriver.Firefox:
        """Create Firefox WebDriver using Selenium's built-in driver manager.
        """
        options = FirefoxOptions()
        if settings.headless:
            options.add_argument("--headless")

        # Selenium 4.6+ has built-in driver manager
        driver = webdriver.Firefox(options=options)
        WebDriverFactory._configure_driver(driver)
        logger.info("Firefox WebDriver created")
        return driver

    @staticmethod
    def _create_edge_driver() -> webdriver.Edge:
        """Create Edge WebDriver using Selenium's built-in driver manager."""
        options = EdgeOptions()
        if settings.headless:
            options.add_argument("--headless")

        # Selenium 4.6+ has built-in driver manager
        driver = webdriver.Edge(options=options)
        WebDriverFactory._configure_driver(driver)
        logger.info("Edge WebDriver created")
        return driver

    @staticmethod
    def _configure_driver(driver: webdriver.Remote) -> None:
        """Configure driver timeouts."""
        driver.implicitly_wait(settings.implicit_wait)
        driver.set_page_load_timeout(settings.page_load_timeout)
        driver.maximize_window()
