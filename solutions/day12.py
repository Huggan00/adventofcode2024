import time
from utils.grids import Grid


def get_input(filename):
    grid = []

    with open("inputs/" + filename, "r") as input:
        for line in input:
            row = []
            for tile in line:
                if tile != "\n":
                    row.append(tile)
            grid.append(row)

    return grid


class Farm(Grid):

    def __init__(self, grid):
        super().__init__(grid)
        self.regions = self.find_regions()

    def find_regions(self):
        regions = []
        searched_tiles = set()
        for tile in self.all():
            if tile in searched_tiles:
                continue
            searched_tiles.add(tile)
            plant_type = self.get(tile)
            region = set()
            self.add_to_region(tile, region, plant_type, searched_tiles)
            regions.append(region)
        return regions

    def add_to_region(self, tile, region, plant_type, searched_tiles):
        if self.get(tile) == plant_type and tile not in region:
            searched_tiles.add(tile)
            region.add(tile)
            for adjacent_tile in self.adjacent(tile):
                self.add_to_region(adjacent_tile, region, plant_type, searched_tiles)

    def find_sides(self, region):
        edges = set()
        sides = []
        for tile in region:
            for other_tile in self.adjacent(tile):
                if other_tile not in region:
                    edges.add((tile, other_tile))
            for outside_tile in self.adjacent_oob(tile):
                edges.add((tile, outside_tile))

        searched_edges = set()

        for edge in edges:
            if edge in searched_edges:
                continue
            side = set()
            self.add_to_side(edge, side, edges, searched_edges)
            sides.append(side)

        return sides

    def add_to_side(self, edge, side, region_edges, searched_edges):
        searched_edges.add(edge)
        side.add(edge)
        for adjacent_edge in self.adjacent_edges(edge):
            if adjacent_edge in region_edges and adjacent_edge not in side:
                self.add_to_side(adjacent_edge, side, region_edges, searched_edges)

    def area(self, region):
        return len(region)

    def perimeter(self, region):
        perimeter = 0
        for tile in region:
            perimeter += len(self.adjacent_oob(tile))
            for other_tile in self.adjacent(tile):
                if other_tile not in region:
                    perimeter += 1
        return perimeter

    def cost_by_perimeter(self):
        total_cost = 0
        for region in self.regions:
            area = self.area(region)
            perimeter = self.perimeter(region)
            cost = area * perimeter
            total_cost += cost

        return total_cost

    def cost_by_sides(self):
        total_cost = 0
        for region in self.regions:
            area = self.area(region)
            num_sides = len(self.find_sides(region))
            cost = area * num_sides
            total_cost += cost

        return total_cost

    def adjacent_oob(self, tile):
        edges = []
        i = tile[0]
        j = tile[1]
        if i == 0:
            edges.append((i - 1, j))
        elif i == self.height - 1:
            edges.append((i + 1, j))
        if j == 0:
            edges.append((i, j - 1))
        if j == self.width - 1:
            edges.append((i, j + 1))
        return edges

    def adjacent_edges(self, edge):
        tile1, tile2 = edge
        i, j = tile1
        k, l = tile2

        if i == k:
            return [((i + 1, j), (k + 1, l)), ((i - 1, j), (k - 1, l))]
        else:
            return [((i, j + 1), (k, l + 1)), ((i, j - 1), (k, l - 1))]


def main():
    start = time.time()

    grid = get_input("day12.txt")

    farm = Farm(grid)

    part1 = farm.cost_by_perimeter()
    print(f"cost without discount: {part1}")
    part2 = farm.cost_by_sides()
    print(f"cost with discount:    {part2}")

    end = time.time()

    duration = end - start
    print(f"Executed in {duration:.3f} seconds")


def tests():

    grid = get_input("day12test.txt")

    farm = Farm(grid)

    part1 = farm.cost_by_perimeter()
    assert part1 == 140

    part2 = farm.cost_by_sides()
    assert part2 == 80

    print("tests passed")


if __name__ == "__main__":

    tests()

    main()
