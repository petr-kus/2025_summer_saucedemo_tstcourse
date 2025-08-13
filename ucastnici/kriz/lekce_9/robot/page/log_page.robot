*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL}              https://www.saucedemo.com/
${USERNAME_INPUT}   //input[@placeholder='Username']
${PASSWORD_INPUT}   //input[@placeholder='Password']
${LOGIN_BUTTON}     //input[@value='Login']

*** Keywords ***
Vyplň Uživatelské Jméno
    [Arguments]    ${username}
    Wait Until Element Is Visible    xpath=${USERNAME_INPUT}    timeout=10s
    Input Text    xpath=${USERNAME_INPUT}    ${username}

Vyplň Heslo
    [Arguments]    ${password}
    Wait Until Element Is Visible    xpath=${PASSWORD_INPUT}    timeout=10s
    Input Text    xpath=${PASSWORD_INPUT}    ${password}

Klikni Na Přihlásit
    Wait Until Element Is Visible    xpath=${LOGIN_BUTTON}    timeout=10s
    Click Button    xpath=${LOGIN_BUTTON}

Zavři Prohlížeč
    Close Browser

Přihlas Uživatele
    [Arguments]    ${username}    ${password}
    Vyplň Uživatelské Jméno    ${username}
    Vyplň Heslo    ${password}
    Klikni Na Přihlásit
    Wait Until Location Contains    /inventory.html    timeout=10s
    Log    Přihlášení uživatele '${username}' bylo úspěšné 
