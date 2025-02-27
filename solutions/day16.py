import time
from utils.grids import Grid
from utils.path_finding import PathFinder, Node

DIRECTIONS = {0: (0, 1), 1: (1, 0), 2: (0, -1), 3: (-1, 0)}


def get_input(filename):

    with open("inputs/" + filename, "r") as input:

        grid = []

        for line in input:
            row = []
            for char in line:
                if char != "\n":
                    row.append(char)
            grid.append(row)

    return grid


class ReindeerState(Node):

    def __init__(self, tile, direction, cost_to_here=0, prev_node=None):
        state = (tile, direction)
        super().__init__(state, cost_to_here, prev_node)


class ReindeerMaze(PathFinder):

    def __init__(self, grid):
        self.grid = Grid(grid)

        for tile in self.grid.all():
            if self.grid.get(tile) == "S":
                self.start_tile = tile
            elif self.grid.get(tile) == "E":
                self.end_tile = tile

    def estimate_cost_to_goal(self, from_node):
        from_tile = from_node.state[0]
        from_direction = from_node.state[1]

        height_steps = abs(self.end_tile[0] - from_tile[0])
        width_steps = abs(self.end_tile[1] - from_tile[1])

        num_turns = 0

        if height_steps > 0:

            num_turns = num_turns_between(from_direction, 3)

        if width_steps > 0:

            num_turns = max(num_turns, num_turns_between(from_direction, 0))

        turns_cost = num_turns * 1000

        return height_steps + width_steps + turns_cost

    def outgoing_edges(self, node):
        for direction in DIRECTIONS:
            vector = DIRECTIONS[direction]
            new_tile = self.grid.move_from(node.state[0], vector)

            if self.grid.get(new_tile) == "#":
                continue

            turn_cost = num_turns_between(node.state[1], direction) * 1000

            new_cost = node.cost_to_here + turn_cost + 1

            yield ReindeerState(new_tile, direction, new_cost, node)

    def solve(self):

        start_node = ReindeerState(self.start_tile, 0)
        cost, paths = self.find_all_paths(start_node)

        optimal_tiles = set()
        for path in paths:
            for state in path:
                tile = state[0]
                optimal_tiles.add(tile)

        num_optimal_tiles = len(optimal_tiles)

        return cost, num_optimal_tiles


def num_turns_between(direction1, direction2):
    turns = abs(direction2 - direction1)

    if turns == 3:
        return 1
    else:
        return turns


def main():

    start = time.time()

    grid = get_input("day16.txt")

    maze = ReindeerMaze(grid)

    part1, part2 = maze.solve()
    assert part1 == 109516
    assert part2 == 568

    end = time.time()

    duration = end - start

    print(f"The cheapest paths have a cost of {part1}")
    print(f"There are {part2} distinct tiles along these paths.")
    print(f"Executed in {duration} seconds")


def tests():
    grid = get_input("day16test.txt")

    maze = ReindeerMaze(grid)

    part1, part2 = maze.solve()

    assert part1 == 7036

    assert part2 == 45

    print("Tests passed")


if __name__ == "__main__":

    tests()

    main()
