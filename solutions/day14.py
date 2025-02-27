import time
import re


HEIGHT = 103
WIDTH = 101


def get_input():

    pattern = r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)"

    with open("inputs/day14.txt", "r") as file:
        input = file.read()

    robot_inputs = re.findall(pattern, input)

    robots = []
    for robot in robot_inputs:
        x = int(robot[0])
        y = int(robot[1])
        v_x = int(robot[2])
        v_y = int(robot[3])

        robots.append(Robot(x, y, v_x, v_y))

    return robots


class Robot:

    def __init__(self, x, y, v_x, v_y):
        self.start_position = (x, y)
        self.velocity = (v_x, v_y)

    def position_after(self, seconds):
        steps_x = self.velocity[0] * seconds
        steps_y = self.velocity[1] * seconds

        new_x = (self.start_position[0] + steps_x) % WIDTH
        new_y = (self.start_position[1] + steps_y) % HEIGHT

        return new_x, new_y


def calc_safety_factor(robots, seconds):
    quadrants = [0, 0, 0, 0]

    for robot in robots:
        end_x, end_y = robot.position_after(seconds)

        if end_x < WIDTH // 2 and end_y < HEIGHT // 2:
            quadrants[0] += 1
        elif end_x > WIDTH // 2 and end_y < HEIGHT // 2:
            quadrants[1] += 1
        elif end_x < WIDTH // 2 and end_y > HEIGHT // 2:
            quadrants[2] += 1
        elif end_x > WIDTH // 2 and end_y > HEIGHT // 2:
            quadrants[3] += 1
        else:
            continue

    return quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]


def print_robots_after(robots, seconds):

    grid = []

    for _ in range(WIDTH):
        row = [0] * HEIGHT
        grid.append(row)

    for robot in robots:
        end_x, end_y = robot.position_after(seconds)

        grid[end_x][end_y] += 1

    for row in grid:
        for elem in row:
            if elem == 0:
                print(".", end="")
            else:
                print(str(elem), end="")
        print("\n", end="")


def calc_max_quadrant_density(robots, seconds):
    quadrants = [0, 0, 0, 0]

    for robot in robots:
        end_x, end_y = robot.position_after(seconds)

        if end_x < WIDTH // 2 and end_y < HEIGHT // 2:
            quadrants[0] += 1
        elif end_x > WIDTH // 2 and end_y < HEIGHT // 2:
            quadrants[1] += 1
        elif end_x < WIDTH // 2 and end_y > HEIGHT // 2:
            quadrants[2] += 1
        elif end_x > WIDTH // 2 and end_y > HEIGHT // 2:
            quadrants[3] += 1
        else:
            continue

    return max(quadrants[0], quadrants[1], quadrants[2], quadrants[3])


def part2(robots):
    densities = []

    for i in range(10000):
        density = calc_max_quadrant_density(robots, i)
        densities.append((density, i))
        print(f"{i}/10000", end="\r")

    densities.sort(key=lambda x: x[0], reverse=True)

    for density in densities:
        second = density[1]
        print_robots_after(robots, second)
        print(second)
        x = input('input "stop" to quit part 2, enter for next map')
        if x == "stop":
            break


if __name__ == "__main__":

    start = time.time()

    robots = get_input()

    part1 = calc_safety_factor(robots, 100)

    part2(robots)

    end = time.time()

    duration = end - start
    print(
        f"The safety factor after 100 steps is {part1}. Executed in {duration} seconds"
    )
