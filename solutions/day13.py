import time
import re


def get_input():

    with open("inputs/day13.txt", "r") as file:
        input = file.read()

    button_a_pattern = r"Button A: X\+(\d+), Y\+(\d+)"
    button_b_pattern = r"Button B: X\+(\d+), Y\+(\d+)"
    prize_pattern = r"Prize: X=(\d+), Y=(\d+)"

    a_buttons = tuples_to_ints(re.findall(button_a_pattern, input))
    b_buttons = tuples_to_ints(re.findall(button_b_pattern, input))
    prizes = tuples_to_ints(re.findall(prize_pattern, input))

    return a_buttons, b_buttons, prizes


def tuples_to_ints(tuples):
    result = [tuple(int(x) for x in tup) for tup in tuples]
    return result


def remeasure(prizes):
    return [tuple(x + 10000000000000 for x in prize) for prize in prizes]


A_COST = 3
B_COST = 1


def calc_cost(a_button, b_button, prize):

    p_x, p_y = prize
    a_x, a_y = a_button
    b_x, b_y = b_button
    det = a_x * b_y - b_x * a_y

    t_a, t_b = b_y, -b_x
    t_c, t_d = -a_y, a_x

    p_xt = t_a * p_x + t_b * p_y
    p_yt = t_c * p_x + t_d * p_y

    if p_xt % det == 0 and p_yt % det == 0:

        p_xt = p_xt // det
        p_yt = p_yt // det

        if p_xt >= 0 and p_yt >= 0:
            return p_xt * A_COST + p_yt * B_COST

    else:
        return 0


if __name__ == "__main__":

    start = time.time()

    a_buttons, b_buttons, prizes = get_input()
    part1_cost = 0
    for a_button, b_button, prize in zip(a_buttons, b_buttons, prizes):
        part1_cost += calc_cost(a_button, b_button, prize)

    new_prizes = remeasure(prizes)

    for i in range(len(prizes)):
        pass

    part2_cost = 0
    for a_button, b_button, prize in zip(a_buttons, b_buttons, new_prizes):
        part2_cost += calc_cost(a_button, b_button, prize)

    end = time.time()

    duration = end - start
    print(
        f"The fewest tokens to win all possible prizes is {part1_cost}, or {part2_cost} after measuring correctly. Executed in {duration} seconds"
    )
