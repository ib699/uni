import itertools

menu = """    1) Add a Characteristic
    2) Add a Abstract Block
    3) Choose a Mode
    00) Exit"""

characteristic_help = """    Pls type a characteristic in the following format:
        <name>=<characteristic>
        example:
            A=hair color
    0) back"""

block_abstract_help = """    Pls type a Abstract Block in the following format:
        <characteristic name>=(<block>, <block>, ...)
        example:
            A=(blue, black, brown, yellow)
    0) back"""

mode_help = """    Pls type a Mode:
    1) ACoC
    2) ECC
    3) BCC
    4) MBCC
    0) back"""


class InputRangeModel:
    def __init__(self):
        self.characteristics = {}
        self.blocks_abstracts = {}
        self.base_choice = {}
        self.multiple_base_choice = {}

    def add_characteristic(self, characteristic):
        key, value = characteristic.split('=')
        self.characteristics[key] = value

    def add_block_abstract(self, block_abstract):
        key, values_str = block_abstract.split('=')
        values = [val.strip() for val in values_str.strip('()').split(',')]
        self.blocks_abstracts[key] = values

    def add_base_choice(self, base_choice):
        key, values_str = base_choice.split('=')
        values = [val.strip() for val in values_str.strip('()').split(',')]
        self.base_choice[key] = values

    def add_multiple_base_choice(self, multiple_base_choice):
        key, values_str = multiple_base_choice.split('=')
        values = [val.strip() for val in values_str.strip('()').split(',')]
        self.multiple_base_choice[key] = values

    def check_characteristic_and_block(self):
        for char in self.characteristics:
            if char not in self.blocks_abstracts:
                return False

        for char in self.blocks_abstracts:
            if char not in self.characteristics:
                return False

        return True

    def working_mode_bcc(self):

        base_choice = tuple(self.base_choice['base'])
        abstract_blocks = [value for key, value in self.blocks_abstracts.items() if isinstance(value, list)]

        # if len(abstract_blocks) == 1:
        #     print(f"Generated BCC Test Cases for {base_choice}:")
        #     for item in abstract_blocks:
        #         print(f"({item})")

        test_cases = []  # Initialize an empty list for test cases

        # Generate test cases by varying one element from the base choice at a time
        for i in range(len(base_choice)):
            for option in abstract_blocks[i]:
                if option != base_choice[i]:
                    # Create a new test case that varies the i-th element
                    new_test_case = list(base_choice)
                    new_test_case[i] = option
                    test_cases.append(tuple(new_test_case))

        return f"Generated BCC Test Cases for {base_choice}: \n{test_cases}\nlenth is {len(test_cases)}"

    def working_mode_ecc(self):

        lists = [value for key, value in self.blocks_abstracts.items() if isinstance(value, list)]

        data = itertools.zip_longest(*lists)

        data_list = [list(t) for t in data]

        var = {}
        for index, item in enumerate(data_list):
            var[index] = 0

        for index, item in enumerate(data_list):
            for inner_index, inner_item in enumerate(item):
                if inner_item is None:
                    data_list[index][inner_index] = data_list[var[inner_index]][inner_index]
                    var[inner_index] += 1

        return f"{data_list} \nTotal is {len(data_list)}"

    def working_mode_acoc(self):

        lists = [value for key, value in self.blocks_abstracts.items() if isinstance(value, list)]
        combinations_dynamic = list(itertools.product(*lists))

        return f"{combinations_dynamic} \nTotal is {len(combinations_dynamic)}"

    def working_mode_mbcc(self):
        values = []
        for bcc in self.multiple_base_choice.values():
            self.base_choice['base'] = bcc
            values.append(self.working_mode_bcc())
        return values


if __name__ == '__main__':
    model = InputRangeModel()
    print("----- Implementation of input domain modeler program ----")

    while True:
        choice = input(menu + "\n    Enter: ")

        if choice == '00':
            exit(0)

        elif choice == '1':
            print(characteristic_help)
            char = input("    Enter: ")
            model.add_characteristic(char)

        elif choice == '2':
            print(block_abstract_help)
            block = input("    Enter: ")
            model.add_block_abstract(block)

        elif choice == '3':
            print(mode_help)
            mode = input("    Enter: ")

            if mode == '0':
                break

            if model.check_characteristic_and_block():
                if mode == '1':
                    print(model.working_mode_acoc())

                elif mode == '2':
                    print(model.working_mode_ecc())

                elif mode == '3':
                    base = input("""    Pls Enter Base Choice: 
    Example: base=(<characteristic 1>, <characteristic 2>, ...)""")
                    model.add_base_choice(base)
                    print(model.working_mode_bcc())

                elif mode == '4':
                    while True:
                        base_choice = input("""    Pls Enter Base Choice: 
    Example: base<name>=(<characteristic 1>, <characteristic 2>, ...)""")
                        if base_choice == '0':
                            break
                        model.add_multiple_base_choice(base_choice)
                    print(model.working_mode_mbcc())
            else:
                print("bad input")
