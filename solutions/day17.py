import time
import re


def get_input(filename):

    with open("inputs/" + filename, "r") as file:

        input = file.read()

    a_pattern = r"Register A: (\d+)"
    b_pattern = r"Register B: (\d+)"
    c_pattern = r"Register C: (\d+)"
    program_pattern = "Program: ([\d,]+)"

    a_register = int(re.search(a_pattern, input).group(1))
    b_register = int(re.search(b_pattern, input).group(1))
    c_register = int(re.search(c_pattern, input).group(1))
    registers = [a_register, b_register, c_register]

    program = [int(i) for i in re.search(program_pattern, input).group(1).split(",")]

    return registers, program


class Computer:

    def __init__(self):

        self.operations = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv,
        }

    def run(self, registers, program):
        self.output = []

        self.a_register = registers[0]
        self.b_register = registers[1]
        self.c_register = registers[2]

        self.instruction_pointer = 0

        while self.instruction_pointer < len(program):
            opcode = program[self.instruction_pointer]
            operation = self.operations[opcode]
            input = program[self.instruction_pointer + 1]

            operation(input)

            self.instruction_pointer += 2

    def print_output(self):
        print_sequence(self.output)

    def combo(self, input):
        if input >= 0 and input <= 3:
            return input
        elif input == 4:
            return self.a_register
        elif input == 5:
            return self.b_register
        elif input == 6:
            return self.c_register

    def adv(self, input):
        numerator = self.a_register
        denominator = 2 ** self.combo(input)
        result = numerator // denominator
        self.a_register = result

    def bxl(self, input):
        self.b_register = self.b_register ^ input

    def bst(self, input):
        self.b_register = self.combo(input) % 8

    def jnz(self, input):
        if self.a_register == 0:
            return
        else:
            self.instruction_pointer = input - 2

    def bxc(self, input):
        self.b_register = self.b_register ^ self.c_register

    def out(self, input):
        self.output.append(self.combo(input) % 8)

    def bdv(self, input):
        numerator = self.a_register
        denominator = 2 ** self.combo(input)
        result = numerator // denominator
        self.b_register = result

    def cdv(self, input):
        numerator = self.a_register
        denominator = 2 ** self.combo(input)
        result = numerator // denominator
        self.c_register = result


def print_sequence(sequence):
    print(",".join(map(str, sequence)))


def find_quine(computer, registers, program, a=0, j=0):
    if j == len(program):
        return a
    for i in range(8):
        if j == 0 and i == 0:
            continue
        new_a = a + i * (8 ** (len(program) - j - 1))
        registers[0] = new_a
        computer.run(registers, program)
        if computer.output[-j - 1] == program[-j - 1]:
            final_a = find_quine(computer, registers, program, new_a, j + 1)
            if final_a:
                return final_a


def main():

    start = time.time()

    computer = Computer()
    registers, program = get_input("day17.txt")

    print("Part 1")
    computer.run(registers, program)
    print("output : ", end="")
    computer.print_output()

    print(f"Part 2")

    a_register = find_quine(computer, registers, program)

    registers[0] = a_register
    print("program: ", end="")
    print_sequence(program)
    print("output : ", end="")
    computer.run(registers, program)
    computer.print_output()
    print(f"value of A: {a_register}")

    end = time.time()

    duration = end - start

    print(f"Executed in {duration} seconds")


def tests():
    computer = Computer()
    test_registers, test_program = get_input("day17test.txt")

    computer.run(test_registers, test_program)

    assert computer.output == [4, 6, 3, 5, 6, 3, 5, 2, 1, 0], "test failed"

    print("Tests passed")


if __name__ == "__main__":

    tests()

    main()
