import unittest
from q1 import InputRangeModel  # Replace with the actual name of your module


class TestInputRangeModel(unittest.TestCase):

    def setUp(self):
        self.model = InputRangeModel()

    def test_add_characteristic(self):
        self.model.add_characteristic('A=hair color')
        self.assertEqual(self.model.characteristics['A'], 'hair color')

    def test_add_block_abstract(self):
        self.model.add_block_abstract('A=(blue, black, brown, yellow)')
        self.assertListEqual(self.model.blocks_abstracts['A'], ['blue', 'black', 'brown', 'yellow'])

    def test_add_base_choice(self):
        self.model.add_base_choice('base=(blue, math, 3, three)')
        self.assertListEqual(self.model.base_choice['base'], ['blue', 'math', '3', 'three'])

    def test_add_multiple_base_choice(self):
        self.model.add_multiple_base_choice('base1=(blue, swe, 1, one)')
        self.model.add_multiple_base_choice('base2=(red, ce, 3, two)')
        self.assertListEqual(self.model.multiple_base_choice['base1'], ['blue', 'swe', '1', 'one'])
        self.assertListEqual(self.model.multiple_base_choice['base2'], ['red', 'ce', '3', 'two'])

    def test_check_characteristic_and_block(self):
        self.model.add_characteristic('A=hair color')
        self.model.add_block_abstract('A=(blue, black, brown, yellow)')
        self.model.add_characteristic("B=major")
        self.model.add_block_abstract("B=(cs, swe, ce, math, ist, st)")
        self.assertTrue(self.model.check_characteristic_and_block())

    def test_check_characteristic_and_block_false_v1(self):
        self.model.add_characteristic('A=hair color')
        self.model.add_block_abstract('A=(blue, black, brown, yellow)')
        self.model.add_block_abstract("B=(cs, swe, ce, math, ist, st)")
        self.assertFalse(self.model.check_characteristic_and_block())

    def test_check_characteristic_and_block_false_v2(self):
        self.model.add_characteristic('A=hair color')
        self.model.add_characteristic("B=major")
        self.model.add_block_abstract("B=(cs, swe, ce, math, ist, st)")
        self.assertFalse(self.model.check_characteristic_and_block())

    def test_working_mode_bcc(self):
        self.model.add_characteristic('A=hair color')
        self.model.add_block_abstract('A=(blue, black, brown, yellow)')
        self.model.add_characteristic("B=major")
        self.model.add_block_abstract("B=(cs, swe, ce, math, ist, st)")
        self.model.add_base_choice('base=(black, swe)')
        self.assertEqual(self.model.working_mode_bcc(), "Generated BCC Test Cases for ('black', 'swe'): \n[('blue', "
                                                        "'swe'), ('brown', 'swe'), ('yellow', 'swe'), ('black', "
                                                        "'cs'), ('black', 'ce'), ('black', 'math'), ('black', 'ist'), "
                                                        "('black', 'st')]\nlenth is 8")
        # Add assertions to check if the test cases are generated correctly

    def test_working_mode_ecc(self):
        self.model.add_characteristic('A=hair color')
        self.model.add_block_abstract('A=(blue, black, brown, yellow)')
        self.model.add_characteristic("B=major")
        self.model.add_block_abstract("B=(cs, swe, ce, math, ist, st)")
        self.assertEqual(self.model.working_mode_ecc(), "[['blue', 'cs'], ['black', 'swe'], ['brown', 'ce'], "
                                                        "['yellow', 'math'], ['blue', 'ist'], ['black', "
                                                        "'st']] \nTotal is 6")
        # Add assertions to check if the ECC mode works correctly

    def test_working_mode_acoc(self):
        self.model.add_characteristic('A=hair color')
        self.model.add_block_abstract('A=(blue, black, brown, yellow)')
        self.model.add_characteristic("B=major")
        self.model.add_block_abstract("B=(cs, swe, ce, math, ist, st)")
        self.assertEqual(self.model.working_mode_acoc(), "[('blue', 'cs'), ('blue', 'swe'), ('blue', 'ce'), ('blue', "
                                                         "'math'), ('blue', 'ist'), ('blue', 'st'), ('black', 'cs'), "
                                                         "('black', 'swe'), ('black', 'ce'), ('black', 'math'), "
                                                         "('black', 'ist'), ('black', 'st'), ('brown', 'cs'), "
                                                         "('brown', 'swe'), ('brown', 'ce'), ('brown', 'math'), "
                                                         "('brown', 'ist'), ('brown', 'st'), ('yellow', 'cs'), "
                                                         "('yellow', 'swe'), ('yellow', 'ce'), ('yellow', 'math'), "
                                                         "('yellow', 'ist'), ('yellow', 'st')] \nTotal is 24")
        # Add assertions to check if the ACoC mode works correctly

    def test_working_mode_mbcc(self):
        self.model.add_characteristic('A=hair color')
        self.model.add_block_abstract('A=(blue, black, brown, yellow)')
        self.model.add_characteristic("B=major")
        self.model.add_block_abstract("B=(cs, swe, ce, math, ist, st)")
        self.model.add_multiple_base_choice('base1=(black, swe)')
        self.model.add_multiple_base_choice('base2=(brown, ist)')
        self.assertIsNotNone(self.model.working_mode_mbcc())
        # Add assertions to check if the MBCC mode works correctly


if __name__ == '__main__':
    unittest.main()
