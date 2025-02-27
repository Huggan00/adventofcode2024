import time
from utils.path_finding import PathFinder, Node


def get_input(filename):

    with open("inputs/" + filename, "r") as input:
        towels_line = next(input).strip("\n")

        towels = towels_line.split(", ")

        next(input)

        designs = []

        for line in input:
            designs.append(line.strip("\n"))

        return towels, designs


class TowelTree(PathFinder):

    def __init__(self, towels):

        self.root = {}

        for towel in towels:
            self.add_towel(towel, self.root)

        self.design_cache = {}

    def add_towel(self, towel, node):
        if towel == "":
            node["end"] = True
            return
        else:
            next_stripe = towel[0]

            if next_stripe not in node:
                node[next_stripe] = {}

            self.add_towel(towel[1:], node[next_stripe])

    def count_possible(self, designs):
        num_possible_designs = 0
        num_possible_arrangements = 0

        for design in designs:
            num_possible_arrangements += self.count_arrangements(design)
            if self.count_arrangements(design) > 0:
                num_possible_designs += 1

        return num_possible_designs, num_possible_arrangements

    def count_arrangements(self, design):

        if design == "":
            return 1

        if design in self.design_cache:
            return self.design_cache[design]

        num_arrangements = 0

        next_towels = self.valid_next_towels(design)

        for towel in next_towels:
            num_stripes = len(towel)

            num_arrangements += self.count_arrangements(design[num_stripes:])

        self.design_cache[design] = num_arrangements
        return num_arrangements

    def valid_next_towels(self, design):

        current_towel = ""
        current_node = self.root

        for stripe in design:

            if stripe in current_node:
                current_node = current_node[stripe]
            else:
                break

            current_towel += stripe
            if "end" in current_node:
                yield current_towel


def main():

    start = time.time()

    towels, designs = get_input("day19.txt")

    tree = TowelTree(towels)

    num_possible_designs, num_possible_arrangements = tree.count_possible(designs)

    print(f"Number of possible designs     : {num_possible_designs}")
    print(f"Number of possible arrangements: {num_possible_arrangements}")

    end = time.time()
    duration = end - start
    print(f"Executed in {duration} seconds")


def tests():

    towels, designs = get_input("day19test.txt")

    tree = TowelTree(towels)

    num_possible_designs, num_possible_arrangements = tree.count_possible(designs)
    assert num_possible_designs == 6
    assert num_possible_arrangements == 16

    print("Tests passed")


if __name__ == "__main__":

    tests()

    main()
