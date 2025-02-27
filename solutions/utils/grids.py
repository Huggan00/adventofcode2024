class Grid:

    def __init__(self, grid):
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0])

    def get(self, tile):
        if self.oob(tile):
            return None
        i = tile[0]
        j = tile[1]
        return self.grid[i][j]

    def set(self, tile, value):
        i = tile[0]
        j = tile[1]
        self.grid[i][j] = value

    def oob(self, tile):
        i = tile[0]
        j = tile[1]
        return i < 0 or j < 0 or i >= self.height or j >= self.width

    def move(self, tile, vector, steps=1):
        return (tile[0] + vector[0] * steps, tile[1] + vector[1] * steps)

    def all(self):
        for i in range(self.height):
            for j in range(self.width):
                yield (i, j)

    def adjacent(self, tile):
        i = tile[0]
        j = tile[1]
        if not self.oob((i + 1, j)):
            yield (i + 1, j)
        if not self.oob((i - 1, j)):
            yield (i - 1, j)
        if not self.oob((i, j + 1)):
            yield (i, j + 1)
        if not self.oob((i, j - 1)):
            yield (i, j - 1)
