*** Settings ***
Library    SeleniumLibrary

*** Keywords ***
Přidej Produkt Do Košíku
    [Arguments]    ${nazev}    ${button_add}
    Log    Do košíku přidávám ${nazev}
    TRY
        Wait Until Element Is Visible    ${button_add}    timeout=10s
        Click Element    ${button_add}
        Log    Tlačítko pro přidání ${nazev} stisknuto
    EXCEPT    ${err}
        Log    Nepodařilo se přidat ${nazev} do košíku: ${err}    level=ERROR
        Fail    Chyba při přidání ${nazev} do košíku
    END

Odeber Produkt Z Košíku
    [Arguments]    ${nazev}    ${button_remove}
    Log    Z košíku odebírám ${nazev}
    TRY
        Wait Until Element Is Visible    ${button_remove}    timeout=10s
        Click Element    ${button_remove}
        Log    Tlačítko pro odebrání ${nazev} stisknuto
    EXCEPT    ${err}
        Log    Nepodařilo se odebrat ${nazev} z košíku: ${err}    level=ERROR
        Fail    Chyba při odebrání ${nazev} z košíku
    END

