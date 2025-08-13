*** Settings ***
Library    SeleniumLibrary
Library    ../PomocneLibrary.py
Library    Collections

*** Variables ***
${CART_BUTTON}               css=#shopping_cart_container a
${CONTINUE_BUTTON}           id=continue-shopping

*** Keywords ***
Otevři Košík Ze Stránky S Produkty
    Log    Otviram stranku kosik
    Wait Until Element Is Visible    ${CART_BUTTON}    timeout=10s
    Click Element                    ${CART_BUTTON}
    Log    Tlacitko kosik stisknuto
    Wait Until Location Contains     cart.html
    Log    okno:cart    

Obsah Košíku
    ${seznam}=    Cart Contents
    RETURN    ${seznam}

Ověř, Že Je Položka V Košíku
    [Arguments]    ${nazev_polozky}
    Log    START: test přítomnosti položky ${nazev_polozky} v košíku    
    ${seznam}=    Obsah Košíku
    Should Contain    ${seznam}    ${nazev_polozky}
    Log    ${nazev_polozky} je v košíku    
    Log    END: test přítomnosti položky ${nazev_polozky} v košíku    

Ověř, Že Položka Není V Košíku
    [Arguments]    ${nazev_polozky}
    Log    START: test nepřítomnosti položky ${nazev_polozky} v košíku    
    ${seznam}=    Obsah Košíku
    Should Not Contain    ${seznam}    ${nazev_polozky}
    Log    ${nazev_polozky} není v košíku    
    Log    END: test nepřítomnosti položky ${nazev_polozky} v košíku    

Zpět Na Stránku S Produkty Z Košíku
    Log    Vracim se do invertory
    Wait Until Element Is Visible    ${CONTINUE_BUTTON}    timeout=10s
    Click Element                    ${CONTINUE_BUTTON}
    Log    Tlacitko zpet stisknuto
    Wait Until Location Contains     inventory.html
    Log    okno:inventory
