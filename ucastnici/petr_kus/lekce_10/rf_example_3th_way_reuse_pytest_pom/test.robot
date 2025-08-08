*** Settings ***
Documentation     A test suite for valid login.
Library           saucedemo/LoginPage.py
Library           SeleniumLibrary

*** Test Cases ***
Login user
    Given Open Page  https://www.saucedemo.com/
    And We Are On Page
    When Login standard_user with secret_sauce
    Then Is User Loged

Login user by selenium lib
    Open Browser  url=https://www.saucedemo.com/  browser=chrome
    Input Text  user-name  standard_user
    Input Text  password  secret_sauce
    Click Button  login-button

Better login by selenium
    Open Browser  url=https://www.saucedemo.com/  browser=chrome
    Another login standard_user with secret_sauce

*** Keywords ***
Login ${username} with ${password}
    Login User  ${username}  ${password}

Another login ${username} with ${password}
    Input Text  user-name  ${username}
    Input Text  password  ${password}
    Click Button  login-button