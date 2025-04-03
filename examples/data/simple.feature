Feature: User login

  Scenario: Login attempt with valid credentials
    Given I navigate to the login page
    When I enter the username "user@example.com"
    And I enter the password "password123"
    Then I am navigated to the homepage