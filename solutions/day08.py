import time


def get_input():
    with open("8/input.txt", "r") as input:
        antennas = {}
        for i, line in enumerate(input):
            for j, character in enumerate(line):
                if character != ".":
                    if character not in antennas:
                        antennas[character] = set()
                    antennas[character].add((i, j))
        width = len(line)
        height = i + 1

    return antennas, height, width


def oob(coords, bounds):
    i, j = coords
    height, width = bounds
    return i < 0 or j < 0 or i >= height or j >= width


if __name__ == "__main__":

    start = time.time()
    antennas, height, width = get_input()
    bounds = (height, width)
    end = time.time()
    input_duration = end - start

    antinodes = set()

    for frequency in antennas:
        for antenna1 in antennas[frequency]:
            for antenna2 in antennas[frequency]:
                if antenna1 == antenna2:
                    continue
                distance = [antenna1[0] - antenna2[0], antenna1[1] - antenna2[1]]
                steps = 0
                while True:
                    antinode_location = (
                        antenna1[0] + steps * distance[0],
                        antenna1[1] + steps * distance[1],
                    )
                    if oob(antinode_location, bounds):
                        break
                    antinodes.add(antinode_location)
                    steps += 1

    end = time.time()
    duration = end - start

    print(
        f"Number of unique antinodes is: {len(antinodes)}, executed in {duration} seconds (of which {input_duration} for reading input)"
    )
