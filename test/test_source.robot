*** Settings ***
Library         String
Test Tags       testttag
Metadata        Author        me,myself and I
Metadata        Longer Value
...             Longer metadata values can be split into multiple
...             rows. Also *simple* _formatting_ is supported.
Test Timeout    1min

*** Variables ***
${MY_VAR}    42

*** Test Cases ***
my_first_testcase
	[Documentation]    This is my first test case
	...
    ...    And this documentation continues. And I made this too short for the first try, now it should be long enough. Right?
	...
	...    Maybe there's something down here too.
	[Tags]    mytag    id:12346
	[Setup]    local setup
	Should Be Equal As Integers    ${42}    ${MY_VAR}
	Sleep    1
	Fail    With this test message.
	[Teardown]    local teardown

another_testcase_in_same_suite
	[Documentation]    This one is just as cool as the first.
	String.Convert To Lower Case    this

*** Keywords ***
local setup
	Log To Console    Precondition

local teardown
	Log To Console    Postcondition

Do Something
	Log    Doing Something!