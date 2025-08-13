*** Settings ***
Library    Browser

*** variables ***
${user_name_filed}  id=user-name
${password_filed}  id=password
${login_button}  id=login-button

*** Keywords ***
Login ${user_name} with ${password}
    Fill Text  ${user_name_filed}  ${user_name}
    Fill Text  ${password_filed}  ${password}
    ${element}  Get Element  ${login_button}
    Take Screenshot
    Click  ${element}