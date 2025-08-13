*** Settings ***
Library           RequestsLibrary
Library           Collections
Library           BuiltIn
Library           OperatingSystem
Library           String
Library           JSONLibrary

*** Variables ***
${BASE_URL}       https://restful-booker.herokuapp.com
${random_index}   1
*** Test Cases ***
Get Random Booking And Log Details
    Create Session    booking    ${BASE_URL}
    
    ${response}=      Get Request    booking    /booking
    Should Be Equal As Integers    ${response.status_code}    200

    ${bookings}=      To JSON    ${response.content}
    ${random_item}=   Get From List    ${bookings}    ${random_index}
    ${booking_id}=    Get From Dictionary    ${random_item}    bookingid

    Log    Using booking id: ${booking_id}

    ${detail_response}=    Get Request    booking    /booking/${booking_id}
    Should Be Equal As Integers    ${detail_response.status_code}    200

    ${json_result}=    To JSON    ${detail_response.content}
    Log    ${json_result}