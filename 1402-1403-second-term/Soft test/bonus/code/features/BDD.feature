# Created by lwall at 5/21/24
Feature: Input Range Modeler
As a user of the Input Range Modeler program
I want to add characteristics, abstract blocks, and base choices
So that I can generate test cases in different working modes

Background:
Given the InputRangeModel is initialized

Scenario: Adding a characteristic
When I add a characteristic "A=hair color"
Then the characteristic "A" should be "hair color" in the model

Scenario: Adding an abstract block
When I add an abstract block "A=(blue, black, brown, yellow)"
Then the abstract block "A" should contain "blue, black, brown, yellow"

Scenario: Checking characteristic and block compatibility
Given I have added a characteristic "A=hair color"
And I have added an abstract block "A=(blue, black, brown, yellow)"
When I check characteristic and block compatibility
Then the result should be True

Scenario: Generating BCC test cases
Given I have added a characteristic "A=hair color"
And I have added an abstract block "A=(blue, black, brown, yellow)"
And I have added a base choice "base=(black, math, 3, three)"
When I generate BCC test cases
Then I should get a list of test cases with length greater than 0

Scenario: Generating ECC test cases
Given I have added multiple abstract blocks
When I generate ECC test cases
Then I should get a list of test cases that are not None

Scenario: Generating ACoC test cases
Given I have added multiple abstract blocks
When I generate ACoC test cases
Then I should get a list of all possible combinations from the abstract blocks

Scenario: Generating MBCC test cases
Given I have added multiple base choices
When I generate MBCC test cases
Then I should get a list of BCC test cases for each base choice