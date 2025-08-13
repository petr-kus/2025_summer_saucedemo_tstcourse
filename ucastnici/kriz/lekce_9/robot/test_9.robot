*** Settings ***
Library    SeleniumLibrary
Library    PomocneLibrary.py
Resource   page/log_page.robot
Resource   page/inventory_page.robot
Resource   page/cart_page.robot

*** Variables ***
${URL}       https://www.saucedemo.com

*** Keywords ***
Create Chrome Options With Disabled Password Manager
    ${options}=    Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys, selenium.webdriver
    ${prefs}=      Create Dictionary    credentials_enable_service=False    profile.password_manager_enabled=False
    Call Method    ${options}    add_experimental_option    prefs    ${prefs}
    RETURN     ${options}

Login With Credentials
    [Arguments]    ${username}    ${password}
    ${options}=    Create Chrome Options With Disabled Password Manager
    Open Browser    ${URL}    chrome    options=${options}
    Maximize Browser Window
    Přihlas Uživatele    ${username}    ${password}    
    Close Browser

Add Remove Product From Cart
    [Arguments]    ${product_name}    ${button_add_locator}    ${button_remove_locator}    ${product_text}
    ${options}=    Create Chrome Options With Disabled Password Manager
    Open Browser    ${URL}    chrome    options=${options}
    Maximize Browser Window
    Přihlas Uživatele    standard_user    secret_sauce
    Přidej Produkt Do Košíku    ${product_name}    ${button_add_locator}
    Otevři Košík Ze Stránky S Produkty
    Ověř, Že Je Položka V Košíku    ${product_text}
    Zpět Na Stránku S Produkty Z Košíku
    Odeber Produkt Z Košíku    ${product_name}    ${button_remove_locator}    
    Ověř, Že Položka Není V Košíku    ${product_text}
    Close Browser

*** Test Cases ***
Login Test - ${username}
    [Template]    Login With Credentials
    standard_user          secret_sauce
    problem_user           secret_sauce
    #locked_out_user        secret_sauce
    #error_user             secret_sauce
    #visual_user            secret_sauce

Add and Remove Product From Cart - ${product_name}
    [Template]    Add Remove Product From Cart
    Sauce Labs Backpack              id=add-to-cart-sauce-labs-backpack       id=remove-sauce-labs-backpack       Sauce Labs Backpack
    Sauce Labs Bolt T-Shirt          id=add-to-cart-sauce-labs-bolt-t-shirt    id=remove-sauce-labs-bolt-t-shirt    Sauce Labs Bolt T-Shirt
    #Sauce Labs Fleece Jacket         id=add-to-cart-sauce-labs-fleece-jacket   id=remove-sauce-labs-fleece-jacket   Sauce Labs Fleece Jacket
    #Sauce Labs Bike Light            id=add-to-cart-sauce-labs-bike-light      id=remove-sauce-labs-bike-light      Sauce Labs Bike Light
