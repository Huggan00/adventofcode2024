import time
from utils.grids import Grid


DIRECTION = {">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0)}


def get_normal_input():
    grid = []

    with open("inputs/day15.txt", "r") as input:

        line = next(input)
        while "#" in line:
            row = []
            for tile in line:
                if tile != "\n":
                    row.append(tile)
            grid.append(row)
            line = next(input)

        rest = input.read()

        moves = []
        for char in rest:
            if char in "^v<>":
                moves.append(char)

    return grid, moves


def get_wide_input():
    grid = []

    with open("inputs/day15.txt", "r") as input:

        line = next(input)
        while "#" in line:
            row = []
            for tile in line:
                if tile != "\n":
                    if tile == "O":
                        row.append("[")
                        row.append("]")
                    elif tile == "@":
                        row.append("@")
                        row.append(".")
                    else:
                        row.append(tile)
                        row.append(tile)
            grid.append(row)
            line = next(input)

        rest = input.read()

        moves = []
        for char in rest:
            if char in "^v<>":
                moves.append(char)

    return grid, moves


class Warehouse(Grid):

    def __init__(self, grid):
        super().__init__(grid)
        for tile in self.all():
            if self.get(tile) == "@":
                self.position = tile
                self.set(tile, ".")
                break

    def step(self, move):

        direction = DIRECTION[move]

        next_tile = self.move_from(self.position, direction)

        if self.get(next_tile) == "#":
            return
        elif self.get(next_tile) == "O":
            chain_end = self.move_from(next_tile, direction)
            while self.get(chain_end) == "O":
                chain_end = self.move_from(chain_end, direction)

            if self.get(chain_end) == "#":
                return

            self.set(chain_end, "O")
            self.set(next_tile, ".")

        self.position = next_tile

    def gps_sum(self):
        sum = 0
        for tile in self.all():
            if self.get(tile) == "O":
                sum += tile[0] * 100 + tile[1]

        return sum

    def print_grid(self):
        for i, row in enumerate(self.grid):
            for j, elem in enumerate(row):
                if self.position == (i, j):
                    print("@", end="")
                elif elem == ".":
                    print(" ", end="")
                else:
                    print(elem, end="")
                print(" ", end="")
            print("\n", end="")


class WideWarehouse(Grid):

    def __init__(self, grid):
        super().__init__(grid)
        for tile in self.all():
            if self.get(tile) == "@":
                self.position = tile
                self.set(tile, ".")
                break

    def step(self, move):
        direction = DIRECTION[move]

        next_tile = self.move_from(self.position, direction)

        if not self.movable(next_tile, direction):
            return

        self.move(next_tile, direction)

        self.position = next_tile

    def movable(self, tile, direction):
        if self.get(tile) == "#":
            return False
        elif self.get(tile) == ".":
            return True

        tiles = {tile}
        if self.get(tile) == "[":
            tiles.add(self.move_from(tile, (0, 1)))
        elif self.get(tile) == "]":
            tiles.add(self.move_from(tile, (0, -1)))

        recursions = []

        for tile in tiles:
            next_tile = self.move_from(tile, direction)
            if next_tile not in tiles:
                recursions.append(self.movable(next_tile, direction))

        return False not in recursions

    def move(self, tile, direction):

        if self.get(tile) == "[":
            tiles = [tile, self.move_from(tile, (0, 1))]
        elif self.get(tile) == "]":
            tiles = [self.move_from(tile, (0, -1)), tile]
        elif self.get(tile) == "#":
            raise Exception("tried to move a wall")
        else:
            return

        for tile in tiles:
            self.set(tile, ".")
            next_tile = self.move_from(tile, direction)
            if next_tile not in tiles:
                self.move(next_tile, direction)

        self.set(self.move_from(tiles[0], direction), "[")
        self.set(self.move_from(tiles[1], direction), "]")

    def gps_sum(self):
        sum = 0
        for tile in self.all():
            if self.get(tile) == "[":
                sum += tile[0] * 100 + tile[1]

        return sum

    def print_grid(self):
        for i, row in enumerate(self.grid):
            for j, elem in enumerate(row):
                if self.position == (i, j):
                    print("@", end="")
                elif elem == ".":
                    print(" ", end="")
                else:
                    print(elem, end="")
                print(" ", end="")
            print("\n", end="")


if __name__ == "__main__":

    start = time.time()

    grid, moves = get_normal_input()

    warehouse = Warehouse(grid)

    for move in moves:
        warehouse.step(move)

    part1 = warehouse.gps_sum()

    wide_grid, moves = get_wide_input()

    warehouse = WideWarehouse(wide_grid)

    for move in moves:
        warehouse.step(move)
        warehouse.print_grid()

    part2 = warehouse.gps_sum()

    end = time.time()

    duration = end - start
    print(
        f"The GPS sum for the normal warehouse is {part1}, for the wide warehouse it is {part2}. Executed in {duration} seconds"
    )
