"""Web step definitions."""

from behave import given, then
from pages.web.landing_page import LandingPage


def _get_page(context) -> LandingPage:
    """Get or create page instance."""
    if not hasattr(context, "page") or not isinstance(context.page, LandingPage):
        context.page = LandingPage(context.driver)
    return context.page


def _get_base_url(context) -> str:
    """Get base URL from settings with validation."""
    base_url = context.settings.base_url
    if not base_url:
        raise ValueError("BASE_URL environment variable is not set.")
    return base_url


@given("I am on the landing page")
def step_am_on_landing_page(context):
    """Navigate to landing page."""
    page = _get_page(context)
    base_url = _get_base_url(context)
    page.navigate_to_landing_page(base_url)


@then("the page title should not be empty")
def step_page_title_not_empty(context):
    """Verify page title is not empty."""
    page = _get_page(context)
    title = page.get_page_title()
    assert title, "Page title should not be empty"


@then("the page URL should contain the base URL")
def step_page_url_contains_base_url(context):
    """Verify page URL contains base URL."""
    page = _get_page(context)
    base_url = _get_base_url(context)
    current_url = page.current_url
    base_url_clean = base_url.rstrip("/")
    assert base_url_clean in current_url, \
        f"Expected URL to contain '{base_url_clean}', got '{current_url}'"
