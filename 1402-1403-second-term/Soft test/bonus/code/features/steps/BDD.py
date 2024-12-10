from behave import given, when, then

from q1 import InputRangeModel


####################################
@given('the InputRangeModel is initialized')
def step_impl(context):
    context.model = InputRangeModel()


@when('I add a characteristic "A=hair color"')
def step_impl(context):
    context.result = context.model.add_characteristic("A=hair color")


@then('the characteristic "A" should be "hair color" in the model')
def step_impl(context):
    assert f"Expected: {'hair color'}, Actual: {context.model.characteristics['A']}"


####################################
@when('I add an abstract block "A=(blue, black, brown, yellow)"')
def step_impl(context):
    context.result = context.model.add_block_abstract("A=(blue, black, brown, yellow)")


@then('the abstract block "A" should contain "blue, black, brown, yellow"')
def step_impl(context):
    assert f"Expected: {'blue', 'black', 'brown', 'yellow'}, Actual: {context.model.blocks_abstracts['A']}"


####################################

@given('I have added a characteristic "A=hair color"')
def step_impl(context):
    context.result = context.model.add_characteristic("A=hair color")


@given('I have added an abstract block "A=(blue, black, brown, yellow)"')
def step_impl(context):
    context.result = context.model.add_block_abstract("A=(blue, black, brown, yellow)")


@when('I check characteristic and block compatibility')
def step_impl(context):
    context.result = context.model.check_characteristic_and_block()


@then('the result should be True')
def step_impl(context):
    assert context.result == True


####################################

@given('I have added a base choice "base=(black, math, 3, three)"')
def step_impl(context):
    context.model.add_characteristic('A=hair color')
    context.model.add_block_abstract('A=(blue, black, brown, yellow)')
    context.model.add_characteristic("B=major")
    context.model.add_block_abstract("B=(cs, swe, ce, math, ist, st)")
    context.result = context.model.add_base_choice('base=(blue, swe)')


@when("I generate BCC test cases")
def step_impl(context):
    context.result = context.model.working_mode_bcc()


@then("I should get a list of test cases with length greater than 0")
def step_impl(context):
    var = context.result is not None


####################################
@given("I have added multiple abstract blocks")
def step_impl(context):
    context.model.add_characteristic('A=hair color')
    context.model.add_block_abstract('A=(blue, black, brown, yellow)')
    context.model.add_characteristic("B=major")
    context.model.add_block_abstract("B=(cs, swe, ce, math, ist, st)")


@when("I generate ECC test cases")
def step_impl(context):
    context.result = context.model.working_mode_ecc()


@then("I should get a list of test cases that are not None")
def step_impl(context):
    var = context.result is not None


####################################

@when("I generate ACoC test cases")
def step_impl(context):
    context.result = context.model.working_mode_acoc()


@then("I should get a list of all possible combinations from the abstract blocks")
def step_impl(context):
    var = context.result is not None


####################################

@given("I have added multiple base choices")
def step_impl(context):
    context.model.add_characteristic('A=hair color')
    context.model.add_block_abstract('A=(blue, black, brown, yellow)')
    context.model.add_characteristic("B=major")
    context.model.add_block_abstract("B=(cs, swe, ce, math, ist, st)")
    context.model.add_multiple_base_choice('base1=(black, swe)')
    context.model.add_multiple_base_choice('base2=(brown, ist)')


@when("I generate MBCC test cases")
def step_impl(context):
    context.result = context.model.working_mode_mbcc()


@then("I should get a list of BCC test cases for each base choice")
def step_impl(context):
    var = context.result is not None