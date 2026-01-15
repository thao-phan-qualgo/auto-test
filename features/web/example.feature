@web @smoke
Feature: Example Web Test
  As a test user
  I want to verify basic web functionality
  So that I can ensure the application works correctly

  Scenario: Verify page loads successfully
    Given I am on the landing page
    Then the page title should not be empty
    And the page URL should contain the base URL
