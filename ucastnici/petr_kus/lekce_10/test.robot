*** Settings ***
Documentation     A test suite for valid login.
Library    Browser
Library    Screenshot
Resource   pages/LoginPage.robot
#Library     test.py
#Library     LoginPage.py

*** Test Cases ***
#Login User with Password
#    ${my_browser}  browser 
#    Login Page  ${my_browser}
#    login user  standard_user  secret_sauce

Login User with Password
    New Browser  chromium  headless=false
    New Page    https://www.saucedemo.com/  wait_until=load
    Take Screenshot
    Login standard_user with secret_sauce
 
*** Keywords ***
Login User
    Fill Text  id=user-name  standard_user
    Fill Text  id=password  secret_sauce
    ${element}  Get Element  id=login-button
    Click  ${element}