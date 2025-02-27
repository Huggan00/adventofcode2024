import time
from copy import deepcopy
from utils.grids import Grid


def get_input():
    grid = []

    with open("inputs/day06.txt", "r") as input:
        for line in input:
            grid.append(line.replace("\n", ""))

    return grid


class LabMap(Grid):
    directions = ("u", "r", "d", "l")

    def __init__(self, grid):
        super().__init__(grid)
        self.traversed_tiles = set()
        self.traversed_tiles_with_direction = set()
        self.tested_potential_obstacles = set()
        self.valid_potential_obstacles = set()
        self.position = self.find_guard()
        self.direction = 0
        self.inside = True
        self.loop = False

    def find_guard(self):
        for i, row in enumerate(self.grid):
            for j, tile in enumerate(row):
                if tile == "^":
                    return (i, j)

    def row(self, i):
        return self.grid[i]

    def column(self, i):
        column_list = [row[i] for row in self.grid]
        column_str = "".join(column_list)

        return column_str

    def turn_right(self):
        self.direction = (self.direction + 1) % 4

    def get_direction(self):
        return self.directions[self.direction]

    def get_next_direction(self):
        return self.directions[(self.direction + 1) % 4]

    def next_tile(self):
        i, j = self.position
        d = self.get_direction()

        if d == "u":
            next_i, next_j = i - 1, j
        elif d == "r":
            next_i, next_j = i, j + 1
        elif d == "d":
            next_i, next_j = i + 1, j
        elif d == "l":
            next_i, next_j = i, j - 1

        return next_i, next_j

    def step(self):
        next_i, next_j = self.next_tile()

        if self.oob(next_i, next_j):
            self.inside = False
        elif self.get(next_i, next_j) == "#":
            self.turn_right()
            self.add_current_tile()
        else:
            self.position = (next_i, next_j)
            self.add_current_tile()

    def add_current_tile(self):
        i, j = self.position

        if self.get(i, j) != "^":
            self.grid[i] = self.grid[i][:j] + "X" + self.grid[i][j + 1 :]

        if (i, j, self.get_direction()) in self.traversed_tiles_with_direction:
            self.loop = True

        self.traversed_tiles.add((i, j))
        self.traversed_tiles_with_direction.add((i, j, self.get_direction()))

    def traverse(self):
        self.add_current_tile()
        self.loop = False
        while self.inside and not self.loop:
            self.step()

    def traverse_with_insertions(self):
        self.add_current_tile()
        while self.inside and not self.loop:
            next_i, next_j = self.next_tile()
            if (
                self.get(next_i, next_j) != "#"
                and (next_i, next_j) not in self.tested_potential_obstacles
            ):
                self.tested_potential_obstacles.add((next_i, next_j))
                self.save_state()
                self.insert_obstacle()
                self.traverse()
                if self.loop:
                    self.valid_potential_obstacles.add((next_i, next_j))
                self.restore_state()
            self.step()

    def insert_obstacle(self):
        next_i, next_j = self.next_tile()

        if self.get(next_i, next_j) == "#":
            self.inside = False
            return

        self.grid[next_i] = (
            self.grid[next_i][:next_j] + "#" + self.grid[next_i][next_j + 1 :]
        )

    def save_state(self):
        self.saved_grid = deepcopy(self.grid)
        self.saved_position = self.position
        self.saved_traversed_tiles = deepcopy(self.traversed_tiles)
        self.saved_traversed_tiles_with_direction = deepcopy(
            self.traversed_tiles_with_direction
        )
        self.saved_direction = self.direction

    def restore_state(self):
        self.grid = self.saved_grid
        self.position = self.saved_position
        self.traversed_tiles = self.saved_traversed_tiles
        self.traversed_tiles_with_direction = self.saved_traversed_tiles_with_direction
        self.direction = self.saved_direction
        self.inside = True
        self.loop = False

    def get_traversed_tiles(self):
        return len(self.traversed_tiles)

    def get_potential_obstacles(self):
        return len(self.valid_potential_obstacles)

    def print_path(self):
        for row in grid:
            print(row)


if __name__ == "__main__":

    grid = get_input()

    start = time.time()

    main = LabMap(grid)
    main.traverse_with_insertions()
    traversed = main.get_traversed_tiles()
    obstacles = main.get_potential_obstacles()

    end = time.time()
    duration = end - start

    print(
        f"Tiles traversed is: {traversed}, potential obstacles is: {obstacles}, executed in {duration} seconds"
    )
