"""Configuration management using Pydantic Settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Browser configuration
    browser: str = Field(default="chrome", description="Browser name (chrome, firefox, edge)")
    headless: bool = Field(default=False, description="Run browser in headless mode")
    implicit_wait: int = Field(default=10, description="Implicit wait timeout in seconds")
    explicit_wait: int = Field(default=30, description="Explicit wait timeout in seconds")
    page_load_timeout: int = Field(default=60, description="Page load timeout in seconds")

    # Application URLs
    base_url: str = Field(description="Application base URL")

    # Allure reporting
    allure_results_dir: str = Field(default="reports/allure-results", description="Allure results directory")
    allure_report_dir: str = Field(default="reports/allure-report", description="Allure report directory")


settings = Settings()
