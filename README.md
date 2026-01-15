# Test Automation Framework

BDD test automation framework using Behave (Python) with Allure reporting and GitHub Actions CI/CD.

## Features

- **BDD Framework**: Behave with Gherkin syntax
- **Page Object Model**: Maintainable and reusable page objects
- **Allure Reporting**: Beautiful test reports with screenshots
- **GitHub Actions**: Automated test execution with report publishing
- **Multi-Browser Support**: Chrome, Firefox, Edge
- **Configuration Management**: Pydantic Settings for environment variables

## Project Structure

```
auto-test/
├── features/                    # BDD features and steps
│   ├── web/                     # Web UI features
│   │   └── *.feature            # Gherkin feature files
│   ├── api/                     # API features
│   ├── steps/                   # Step definitions
│   │   └── *_steps.py          # Step definition files
│   └── environment.py           # Behave hooks
│
├── pages/                       # Page Object Model
│   ├── base_page.py            # Base page class
│   ├── web/                    # Web page objects
│   │   └── *_page.py           # Page objects
│   └── components/             # Reusable components
│
├── core/                        # Core framework
│   ├── config.py               # Settings management
│   ├── logger.py               # Logging setup
│   └── drivers/                # WebDriver management
│
├── utils/                       # Utilities
├── test_data/                   # Test data files
├── reports/                     # Test reports
│   ├── allure-results/         # Allure results
│   └── allure-report/          # Generated Allure reports
│
├── .github/workflows/           # GitHub Actions
│   └── test.yml                # CI/CD workflow
│
├── behave.ini                   # Behave configuration
├── requirements.txt             # Python dependencies
└── Makefile                     # Common commands
```

## Setup

### Prerequisites

- Python 3.11+
- pip
- Git

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd auto-test
```

2. Create virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
make install
# or
pip install -r requirements.txt
```

4. Install Allure (for local report generation):
```bash
# macOS
brew install allure

# Linux
wget https://github.com/allure-framework/allure2/releases/download/2.24.1/allure-2.24.1.tgz
tar -zxvf allure-2.24.1.tgz
sudo mv allure-2.24.1 /opt/allure
sudo ln -s /opt/allure/bin/allure /usr/local/bin/allure
```

5. Create `.env` file:
```bash
cp env.example .env
# Edit .env with your configuration
```

## Configuration

Edit `.env` file with your settings:

```bash
# Browser Configuration
BROWSER=chrome                    # chrome, firefox, edge
HEADLESS=false                    # true for headless mode
IMPLICIT_WAIT=10                  # Implicit wait in seconds
EXPLICIT_WAIT=30                  # Explicit wait in seconds
PAGE_LOAD_TIMEOUT=60              # Page load timeout in seconds

# Application URLs
BASE_URL=https://example.com      # Your application URL

# Allure Reporting
ALLURE_RESULTS_DIR=reports/allure-results
ALLURE_REPORT_DIR=reports/allure-report
```

## Usage

### Run Tests

```bash
# Run all tests
make test
# or
behave

# Run specific feature
behave features/web/example.feature

# Run with tags
behave --tags @smoke
behave --tags @web
```

### Generate Allure Report

```bash
# Generate report locally
make allure-report
# or
allure generate reports/allure-results -o reports/allure-report --clean

# Open report in browser
allure open reports/allure-report
```

### Code Quality

```bash
# Format code
make format

# Run linters
make lint
```

## Writing Tests

### Feature File (Gherkin)

```gherkin
@web @smoke
Feature: User Login
  As a user
  I want to login to the application
  So that I can access my account

  Scenario: Successful login
    Given I am on the login page
    When I enter valid credentials
    Then I should be redirected to the dashboard
```

### Step Definitions

```python
from behave import given, when, then
from pages.web.login_page import LoginPage

@given("I am on the login page")
def step_on_login_page(context):
    page = LoginPage(context.driver)
    page.navigate_to_login(context.settings.base_url)
    context.page = page
```

### Page Objects

```python
from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class LoginPage(BasePage):
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    def enter_email(self, email: str):
        self.type(self.EMAIL_INPUT, email)
        return self

    def enter_password(self, password: str):
        self.type(self.PASSWORD_INPUT, password)
        return self

    def click_login(self):
        self.click(self.LOGIN_BUTTON)
        return self
```

## GitHub Actions

The workflow automatically:
1. Sets up Python and Allure
2. Installs dependencies
3. Runs tests
4. Generates Allure report
5. Uploads report as artifact
6. Publishes report to GitHub Pages (if configured)

View reports in:
- **Artifacts**: Download from Actions tab
- **GitHub Pages**: If configured, view at `https://<username>.github.io/<repo>/`

## Makefile Commands

```bash
make install       # Install dependencies
make test          # Run all tests
make format        # Format code with black and isort
make lint          # Run flake8 and mypy checks
make clean         # Clean generated files
make allure-report # Generate Allure report
```

## Best Practices

1. **Page Object Model**: Keep page logic in page objects, not step definitions
2. **Thin Steps**: Step definitions should only call page object methods
3. **No Hardcoded Data**: Use `.env` for configuration and test data files
4. **Explicit Waits**: Always use explicit waits, never sleep()
5. **Descriptive Names**: Use clear, descriptive names for features, scenarios, and steps
6. **Tags**: Use tags to categorize tests (@smoke, @regression, @web, @api)

## Troubleshooting

### WebDriver Issues

If you encounter WebDriver issues, ensure:
- Browser drivers are up to date (webdriver-manager handles this automatically)
- Browser version matches driver version
- Firewall/antivirus isn't blocking WebDriver

### Allure Report Not Generating

- Ensure `reports/allure-results` directory exists and contains results
- Check Allure is installed: `allure --version`
- Verify `behave.ini` has correct Allure formatter configuration

## License

[Your License Here]