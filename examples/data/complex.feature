Feature: User Login
Describes the process of logging into a web application for an average user.

  Rule: Only registered users can log in
  Users must have a registered account to log in to the application.

    Background:
    The default assumption is that the user is trying to log in with their email and password.
      Given the user accounts are registered with the following details:
      | username          | password    |
      | user@example.com  | password123 |
      And the admin accounts are registered with the following details:
      | username           | password    |
      | admin@example.com  | password135 |

        @web
        @admin @user
        Scenario: Login attempt with valid credentials
          Given the user navigates to the login page
          And the user enters the username "user@example.com"
          * the user enters the password "password123"
          When the user clicks the "Log In" button
          Then the user is navigated to the homepage
          And the following message is displayed:
          """
            Welcome in our application.
            Feel free to connect with other people, companies and organisations.
          """
          And the following header links are available:
          | header_link |
          | About Us    |
          | Contact     |
          | Profile     |
          When the user logs out
          Then the user is navigated to the login page
          When the user enters the username "admin@example.com"
          And the user enters the password "password135"
          Then the user is navigated to the admin page
          And the following message is displayed: "Admin console."
          But the following message is not displayed:
          """
            Welcome in our application.
            Feel free to connect with other people, companies and organisations.
          """

        Scenario Outline: Login attempt with invalid credentials
        This scenario does not include all failure cases, only selected ones.
          Given the user navigates to the login page
          And the user enters the username "<username>"
          * the user enters the password "<password>"
          When the user clicks the "Log In" button
          Then the following error message is displayed: "<error_message>"

        Scenarios:
          | username            | password | error_message                      |
          | invalid@example.com | valid    | Incorrect username or password     |
          | user@example.com    | invalid  | Incorrect username or password     |
          |                     | valid    | Username is required               |
          | user@example.com    |          | Password is required               |
          |                     |          | Username and password are required |
