import time
from utils.grids import Grid


directions = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))


def get_input(filename):
    grid = []

    with open("inputs/" + filename, "r") as input:
        for line in input:
            grid.append(line.replace("\n", ""))

    return grid


class WordSearch(Grid):

    def __init__(self, grid):
        super().__init__(grid)

    def check_all(self):
        total_sum = 0
        for x in range(self.height):
            for y in range(self.width):
                tile = (x, y)
                total_sum += self.check_space(tile)

        return total_sum


class WordSearchXMAS(WordSearch):

    def check_word(self, tile, direction):

        if self.oob(tile) or self.oob(self.move_from(tile, direction, 3)):
            return False

        x = self.get(tile)
        m = self.get(self.move_from(tile, direction, 1))
        a = self.get(self.move_from(tile, direction, 2))
        s = self.get(self.move_from(tile, direction, 3))

        return x + m + a + s == "XMAS"

    def check_space(self, tile):
        space_sum = 0
        for d in directions:
            if self.check_word(tile, d):
                space_sum += 1

        return space_sum


class WordSearchCrossMAS(WordSearch):

    def slash(self, tile):

        m = self.get(self.move_from(tile, (-1, 1)))
        a = self.get(tile)
        s = self.get(self.move_from(tile, (1, -1)))

        return m + a + s == "MAS" or s + a + m == "MAS"

    def back_slash(self, tile):

        m = self.get(self.move_from(tile, (-1, -1)))
        a = self.get(tile)
        s = self.get(self.move_from(tile, (1, 1)))

        return m + a + s == "MAS" or s + a + m == "MAS"

    def check_space(self, tile):

        if self.oob(self.move_from(tile, (-1, -1))) or self.oob(
            self.move_from(tile, (1, 1))
        ):
            return False

        return self.slash(tile) and self.back_slash(tile)


def main():

    start = time.time()

    grid = get_input("day04.txt")

    word_search = WordSearchXMAS(grid)

    sum = word_search.check_all()

    print("total number of XMAS:  " + str(sum))

    word_search = WordSearchCrossMAS(grid)

    sum = word_search.check_all()

    print("total number of X-MAS: " + str(sum))

    end = time.time()
    duration = end - start
    print(f"Executed in {duration} seconds")


def tests():

    grid = get_input("day04test.txt")

    word_search = WordSearchXMAS(grid)

    sum = word_search.check_all()
    assert sum == 18

    word_search = WordSearchCrossMAS(grid)

    sum = word_search.check_all()
    assert sum == 9

    print("Tests passed")


if __name__ == "__main__":

    tests()

    main()
