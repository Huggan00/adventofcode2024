import time
from utils.grids import Grid
from utils.path_finding import PathFinder, Node


def get_input(filename):
    bytes = []

    with open("inputs/" + filename, "r") as input:

        for line in input:
            byte = tuple(map(int, line.split(",")))
            bytes.append(byte)

    return bytes


class ByteMaze(PathFinder):

    def __init__(self, bytes, coordinate_max):
        self.bytes = bytes
        self.size = coordinate_max + 1

    def set_grid(self, time):
        grid = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append(".")
            grid.append(row)

        for i in range(min(len(self.bytes), time)):
            row = self.bytes[i][0]
            col = self.bytes[i][1]
            grid[row][col] = "#"

        self.grid = Grid(grid)

    def estimate_cost_to_goal(self, from_node):
        height_distance = (self.size - 1) - from_node.state[0]
        width_distance = (self.size - 1) - from_node.state[1]
        return height_distance + width_distance

    def outgoing_edges(self, node: Node):
        node_tile = node.state
        for adjacent_tile in self.grid.adjacent(node_tile):
            if self.grid.get(adjacent_tile) != "#":
                cost = node.cost_to_here + 1
                outgoing_edge = Node(
                    state=adjacent_tile, cost_to_here=cost, prev_node=node
                )
                yield outgoing_edge

    def find_path_at_time(self, time):
        self.set_grid(time)

        start_node = Node(state=(0, 0))
        return self.find_path(start_node)

    def find_time_limit(self, start_time):

        cost, _ = self.find_path_at_time(start_time)

        if cost < 0:
            return None

        time_high = len(self.bytes)
        time_low = start_time

        while time_low < time_high:
            mid = (time_high + time_low) // 2

            cost, _ = self.find_path_at_time(mid)

            if cost < 0:
                time_high = mid
            else:
                time_low = mid + 1

        return self.bytes[time_low - 1]


def print_path(grid, path):
    path = set(path)
    for i, row in enumerate(grid):
        for j, elem in enumerate(row):
            if (i, j) in path:
                print(".", end="")
            elif elem == ".":
                print(" ", end="")
            else:
                print(elem, end="")
            print(" ", end="")
        print("\n", end="")
    print("\n", end="")


def main():

    start = time.time()

    bytes = get_input("day18.txt")

    maze = ByteMaze(bytes, 70)

    part1_cost, path = maze.find_path_at_time(1024)
    print_path(maze.grid.grid, path)
    print(f"The cheapest path has a cost of {part1_cost}")

    last_byte = maze.find_time_limit(start_time=1024)
    byte_x = last_byte[0]
    byte_y = last_byte[1]
    print(f"The byte that cuts off the last path is ({byte_x},{byte_y})")

    end = time.time()
    duration = end - start
    print(f"Executed in {duration} seconds")


def tests():
    bytes = get_input("day18test.txt")

    maze = ByteMaze(bytes, 6)

    cost, path = maze.find_path_at_time(12)
    assert cost == 22

    last_byte = maze.find_time_limit(start_time=12)
    assert last_byte == (6, 1)

    print("Tests passed")


if __name__ == "__main__":

    tests()

    main()
