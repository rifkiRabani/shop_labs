Feature: Login
  As a registered user
  I want to log in to the shop
  So that I can access my dashboard

  Scenario: Login with valid credentials
    Given the user is on the login page
    When the user logs in with email "demo@demo.com" and password "demo"
    Then the dashboard should be open

  Scenario: Login with invalid username
    Given the user is on the login page
    When the user submits username "invalid_username" and password "valid_password"
    Then the dashboard should not be open
