import time
from enum import Enum
import re


def get_input():
    calibrations = []

    pattern = "[0-9]+"
    with open("inputs/day07.txt", "r") as input:
        for line in input:
            matches = re.findall(pattern, line)
            numbers = [int(match) for match in matches]
            calibrations.append(numbers)

    return calibrations


class Operators(Enum):
    addition = 1
    multiplication = 2
    concatenation = 3

    def next(self):
        enum_members = list(Operators)
        current_index = enum_members.index(self)
        next_index = (current_index + 1) % len(enum_members)
        return enum_members[next_index]


def generate_operators(n):
    operators = [Operators(1) for _ in range(n)]
    done = False

    while not done:
        yield operators

        i = 0
        while True:
            operators[i] = operators[i].next()
            if operators[i].value == 1:
                i += 1
                if i == len(operators):
                    done = True
                    break
            else:
                break


def apply_operator(operator, first_operand, second_operand):

    if operator == Operators.addition:
        return first_operand + second_operand
    elif operator == Operators.multiplication:
        return first_operand * second_operand
    elif operator == Operators.concatenation:
        return int(str(first_operand) + str(second_operand))


def validate_calibration(wanted_result, operands):

    num_operators = len(operands) - 1

    for operators in generate_operators(num_operators):
        current_result = operands[0]
        for i in range(len(operators)):
            current_result = apply_operator(
                operators[i], current_result, operands[i + 1]
            )
        if current_result == wanted_result:
            return True
    return False


if __name__ == "__main__":

    calibrations = get_input()

    start = time.time()

    sum = 0
    for calibration in calibrations:
        if validate_calibration(calibration[0], calibration[1:]):
            sum += calibration[0]

    end = time.time()
    duration = end - start

    print(f"Number of valid calibrations is: {sum}, executed in {duration} seconds")
