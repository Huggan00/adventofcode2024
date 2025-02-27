import time


def get_input():
    with open("inputs/day11simon.txt", "r") as input:
        line = input.readline()
        engravings = line.split()

    stones = {}
    for engraving in engravings:
        stones[engraving] = 1

    return stones


def blink(stones):
    new_stones = {}
    for engraving in stones:
        new_engravings = []
        num_engravings = stones[engraving]
        num_digits = len(engraving)
        if engraving == "0":
            new_engravings.append("1")
        elif num_digits % 2 == 0:
            first_engraving = engraving[: num_digits // 2]
            second_engraving = engraving[num_digits // 2 :]
            second_engraving = remove_leading_zeroes(second_engraving)
            new_engravings.append(first_engraving)
            new_engravings.append(second_engraving)
        else:
            engraving = int(engraving)
            engraving = engraving * 2024
            engraving = str(engraving)
            new_engravings.append(engraving)

        for new_engraving in new_engravings:
            if new_engraving not in new_stones:
                new_stones[new_engraving] = num_engravings
            else:
                new_stones[new_engraving] += num_engravings

    return new_stones


def stone_sum(stones):
    sum = 0
    for value in stones.values():
        sum += value
    return sum


def remove_leading_zeroes(engraving):
    while len(engraving) > 1 and engraving[0] == "0":
        engraving = engraving[1:]
    return engraving


if __name__ == "__main__":
    stones = get_input()

    start = time.time()

    for i in range(1, 26):
        stones = blink(stones)
        print(f"blinked {i} times", end="\r")

    part1 = stone_sum(stones)

    for i in range(26, 76):
        stones = blink(stones)
        print(f"blinked {i} times", end="\r")

    part2 = stone_sum(stones)

    end = time.time()

    duration = end - start
    print(
        f"The number of stones after 25 blinks is {part1}, the number after 75 is {part2}, executed in {duration} seconds"
    )
