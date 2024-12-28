Feature: OrangeHRM Login 

@LGN-1201
Scenario: To verify login with valid credentials
    Given the user is on the OrangeHRM landing page
    When the user enters "admin" as the username and "admin123" as the password
    And clicks the Login button
    Then the user is navigated to the homepage

@LGN-1202
Scenario: To verify login with valid username and invalid password
    Given the user is on the OrangeHRM landing page
    When the user enters "admin" as the username and "invalid-password" as the password
    And clicks the Login button
    Then the user gets an error message "Invalid credentials"

@LGN-1203
Scenario: To verify login with invalid username and invalid password
    Given the user is on the OrangeHRM landing page
    When the user enters "invalid-user" as the username and "invalid-password" as the password
    And clicks the Login button
    Then the user gets an error message "Invalid credentials"