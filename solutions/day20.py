import time
from utils.grids import Grid


def get_input(filename):

    grid = []

    with open("inputs/" + filename, "r") as input:

        for line in input:
            row = []
            for char in line:
                if char != "\n":
                    row.append(char)
            grid.append(row)

    return grid


class RaceTrack(Grid):

    def __init__(self, grid):
        super().__init__(grid)
        self.tile_time = self._build_path()

    def _find_start(self):
        for tile in self.all():
            if self.get(tile) == "S":
                return tile

    def _build_path(self):
        tile_time = {}

        current_tile = self._find_start()

        i = 0
        while True:
            tile_time[current_tile] = i
            i += 1

            if self.get(current_tile) == "E":
                return tile_time

            for other_tile in self.adjacent(current_tile):
                if self.get(other_tile) != "#" and other_tile not in tile_time:
                    current_tile = other_tile
                    break

    def find_all_2ps_shortcuts(self, min_timesave=1):
        num_shortcuts = 0
        directions = ((0, 1), (0, -1), (1, 0), (-1, 0))

        for start in self.tile_time:
            for direction in directions:
                end = self.move(start, direction, 2)

                if end in self.tile_time:
                    saved_time = self.tile_time[end] - self.tile_time[start] - 2

                    if saved_time >= min_timesave:
                        num_shortcuts += 1

        return num_shortcuts

    def find_all_20ps_shortcuts(self, min_timesave=1):
        num_shortcuts = 0

        for start in self.tile_time:
            for x_steps in range(-20, 21):
                for y_steps in range(-20 + abs(x_steps), 21 - abs(x_steps)):
                    end = self.move(start, (x_steps, y_steps))

                    if end in self.tile_time:
                        saved_time = (
                            self.tile_time[end]
                            - self.tile_time[start]
                            - (abs(x_steps) + abs(y_steps))
                        )

                        if saved_time >= min_timesave:
                            num_shortcuts += 1

        return num_shortcuts


def main():

    start = time.time()

    grid = get_input("day20.txt")

    race = RaceTrack(grid)

    num_2ps_shortcuts = race.find_all_2ps_shortcuts(100)
    num_20ps_shortcuts = race.find_all_20ps_shortcuts(100)

    print(f"number of 2ps shortcuts saving at least 100 seconds : {num_2ps_shortcuts}")
    print(f"number of 20ps shortcuts saving at least 100 seconds: {num_20ps_shortcuts}")

    end = time.time()
    duration = end - start
    print(f"Executed in {duration} seconds")


def tests():

    grid = get_input("day20test.txt")

    race = RaceTrack(grid)

    num_shortcuts = race.find_all_2ps_shortcuts()
    num_shortcuts_min_3 = race.find_all_2ps_shortcuts(3)
    num_shortcuts_min_64 = race.find_all_2ps_shortcuts(64)

    assert num_shortcuts == 44
    assert num_shortcuts - num_shortcuts_min_3 == 14
    assert num_shortcuts_min_64 == 1

    num_shortcuts_min_50 = race.find_all_20ps_shortcuts(50)
    num_shortcuts_min_51 = race.find_all_20ps_shortcuts(51)
    num_shortcuts_min_74 = race.find_all_20ps_shortcuts(74)
    num_shortcuts_min_76 = race.find_all_20ps_shortcuts(76)

    num_shortcuts_50 = num_shortcuts_min_50 - num_shortcuts_min_51
    num_shortcuts_74 = num_shortcuts_min_74 - num_shortcuts_min_76

    assert num_shortcuts_50 == 32
    assert num_shortcuts_74 == 4
    assert num_shortcuts_min_76 == 3

    print("Tests passed")


if __name__ == "__main__":

    tests()

    main()
