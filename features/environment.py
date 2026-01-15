"""Behave environment configuration and hooks."""

import os
from behave import fixture, use_fixture
from selenium.webdriver.remote.webdriver import WebDriver

from core.drivers.webdriver_factory import WebDriverFactory
from core.config import settings
from core.logger import logger


@fixture
def browser_driver(context, **kwargs) -> WebDriver:
    """Create WebDriver instance before scenario."""
    logger.info("Setting up WebDriver...")
    driver = WebDriverFactory.create_driver()
    context.driver = driver
    context.settings = settings
    yield driver
    logger.info("Tearing down WebDriver...")
    driver.quit()


def before_all(context):
    """Run before all scenarios."""
    logger.info("=" * 80)
    logger.info("Starting test execution")
    logger.info("=" * 80)


def after_all(context):
    """Run after all scenarios."""
    logger.info("=" * 80)
    logger.info("Test execution completed")
    logger.info("=" * 80)


def before_feature(context, feature):
    """Run before each feature."""
    logger.info(f"Feature: {feature.name}")


def after_feature(context, feature):
    """Run after each feature."""
    logger.info(f"Feature completed: {feature.name}")


def before_scenario(context, scenario):
    """Run before each scenario."""
    use_fixture(browser_driver, context)
    logger.info(f"Scenario: {scenario.name}")


def after_scenario(context, scenario):
    """Run after each scenario."""
    if scenario.status == "failed":
        logger.error(f"Scenario failed: {scenario.name}")
        # Take screenshot on failure
        screenshot_dir = "reports/screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        filename = scenario.name.replace(" ", "_") + ".png"
        screenshot_path = f"{screenshot_dir}/{filename}"
        context.driver.save_screenshot(screenshot_path)
        logger.info(f"Screenshot saved: {screenshot_path}")
    else:
        logger.info(f"Scenario passed: {scenario.name}")
