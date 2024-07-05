from q1 import InputRangeModel

# Example of how to use the InputRangeModel class
model = InputRangeModel()
model.add_characteristic("A=hair color")
model.add_characteristic("B=major")
model.add_characteristic("C=number")
model.add_characteristic("D=num in text")
model.add_characteristic("E=total")
model.add_block_abstract("A=(blue, black, brown, yellow)")
model.add_block_abstract("B=(cs, swe, ce, math, ist, st)")
model.add_block_abstract("C=(1, 2, 3, 4)")
model.add_block_abstract("D=(one, two, three)")
model.add_block_abstract("E=(29, 54)")

# Call different working modes
if model.check_characteristic_and_block():

    model.add_base_choice("base=(black, math, 3)")
    print(model.working_mode_bcc())

    ##
    model.add_multiple_base_choice("base1=(black, math, 3)")
    model.add_multiple_base_choice("base2=(brown, ce, 2)")
    print(model.working_mode_mbcc())

    # done
    print(model.working_mode_ecc())

    # done
    print(model.working_mode_acoc())