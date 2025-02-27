import time


def get_input(filename):

    with open("inputs/" + filename, "r") as input:
        program = input.read()

    return program


def parse_number(line, i):
    if not line[i].isnumeric():
        return 0, 0

    number_length = 0
    digits = []

    k = 0
    while i + k < len(line) and k < 3:

        if line[i + k].isnumeric():
            digits.append(int(line[i + k]))
            number_length += 1
            k += 1
        else:
            break

    number = 0
    for j in range(number_length):
        number += 10**j * digits[-1 - j]

    return number_length, number


def sum_all_mul(program):
    sum = 0
    for i in range(len(program)):
        if program[i : i + 4] == "mul(":

            first_number_length, first_number = parse_number(program, i + 4)
            second_number_length, second_number = parse_number(
                program, i + 4 + first_number_length + 1
            )
            if (
                first_number_length == 0
                or second_number_length == 0
                or program[i + 4 + first_number_length] != ","
                or program[i + 4 + first_number_length + 1 + second_number_length]
                != ")"
            ):
                continue
            sum += first_number * second_number
    return sum


def sum_enabled_mul(program):
    sum = 0
    enabled = True
    for i in range(len(program)):

        if program[i : i + 4] == "do()":
            enabled = True
        elif program[i : i + 7] == "don't()":
            enabled = False
        if program[i : i + 4] == "mul(" and enabled:

            first_number_length, first_number = parse_number(program, i + 4)
            second_number_length, second_number = parse_number(
                program, i + 4 + first_number_length + 1
            )
            if (
                first_number_length == 0
                or second_number_length == 0
                or program[i + 4 + first_number_length] != ","
                or program[i + 4 + first_number_length + 1 + second_number_length]
                != ")"
            ):
                continue
            sum += first_number * second_number
    return sum


def main():

    start = time.time()

    program = get_input("day03.txt")

    part_1 = sum_all_mul(program)
    print("Sum of all multiplications    : " + str(part_1))

    part_2 = sum_enabled_mul(program)
    print("Sum of enabled multiplications: " + str(part_2))

    end = time.time()
    duration = end - start
    print(f"Executed in {duration} seconds")


def tests():
    program = get_input("day03test.txt")

    sum_all = sum_all_mul(program)
    assert sum_all == 161

    sum_enabled = sum_enabled_mul(program)
    assert sum_enabled == 48

    print("Tests passed")


if __name__ == "__main__":

    tests()

    main()
