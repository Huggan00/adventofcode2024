import time


def get_input():
    grid = []

    with open("day10/input.txt", "r") as input:
        for line in input:
            row = []
            for tile in line:
                if tile != "\n":
                    row.append(int(tile))
            grid.append(row)

    return grid


class TrailFinder:

    def __init__(self, grid):
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0])

    def oob(self, i, j):
        return i < 0 or j < 0 or i >= self.height or j >= self.width

    def get(self, i, j):
        if self.oob(i, j):
            return -1
        else:
            return self.grid[i][j]

    def walk(self, i, j, wanted_elevation, visited):
        elevation = self.get(i, j)

        if elevation != wanted_elevation or (i, j) in visited:
            return 0

        visited.add((i, j))

        if elevation == 9:
            return 1
        else:
            return (
                self.walk(i + 1, j, elevation + 1, visited)
                + self.walk(i - 1, j, elevation + 1, visited)
                + self.walk(i, j + 1, elevation + 1, visited)
                + self.walk(i, j - 1, elevation + 1, visited)
            )

    def unique_walk(self, i, j, wanted_elevation):
        elevation = self.get(i, j)

        if elevation != wanted_elevation:
            return 0

        if elevation == 9:
            return 1
        else:
            return (
                self.unique_walk(i + 1, j, elevation + 1)
                + self.unique_walk(i - 1, j, elevation + 1)
                + self.unique_walk(i, j + 1, elevation + 1)
                + self.unique_walk(i, j - 1, elevation + 1)
            )

    def find_trails(self):
        num_found_trails = 0
        for i in range(self.height):
            for j in range(self.width):
                elevation = self.get(i, j)

                if elevation == 0:
                    num_found_trails += self.walk(i, j, 0, set())

        return num_found_trails

    def find_unique_trails(self):
        num_found_trails = 0
        for i in range(self.height):
            for j in range(self.width):
                elevation = self.get(i, j)

                if elevation == 0:
                    num_found_trails += self.unique_walk(i, j, 0)

        return num_found_trails


if __name__ == "__main__":
    start = time.time()
    grid = get_input()
    end = time.time()
    duration = end - start
    print(f"Reading input took {duration} seconds")

    start = time.time()

    trail_finder = TrailFinder(grid)
    num_trails = trail_finder.find_trails()
    num_unique_trails = trail_finder.find_unique_trails()

    end = time.time()
    duration = end - start
    print(
        f"The number of hiking trails is {num_trails}, the number of unique trails is {num_unique_trails}, executed in {duration} seconds"
    )
