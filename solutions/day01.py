import time


def get_input(filename):
    list1, list2 = [], []

    with open("inputs/" + filename, "r") as input:
        for line in input:
            values = line.split()
            list1.append(int(values[0]))
            list2.append(int(values[1]))

    return list1, list2


def get_distance(list1, list2):
    list1, list2 = sorted(list1), sorted(list2)

    total_diff = 0
    for id1, id2 in zip(list1, list2):
        diff = abs(id1 - id2)
        total_diff += diff

    return total_diff


def get_frequencies(list):
    frequencies = {}
    for value in list:
        if value in frequencies:
            frequencies[value] += 1
        else:
            frequencies[value] = 1

    return frequencies


def get_similarity(list1, list2):
    frequencies1 = get_frequencies(list1)
    frequencies2 = get_frequencies(list2)

    total_similarity = 0
    for value in frequencies1:
        if value in frequencies2:
            frequency1 = frequencies1[value]
            frequency2 = frequencies2[value]
            similarity = value * frequency1 * frequency2
            total_similarity += similarity

    return total_similarity


def main():

    start = time.time()

    list1, list2 = get_input("day01.txt")

    distance = get_distance(list1, list2)
    print("Summed distance: " + str(distance))

    similarity = get_similarity(list1, list2)
    print("Similarity: " + str(similarity))

    end = time.time()

    duration = end - start

    print(f"executed in {duration:.3f} seconds")


def tests():

    list1, list2 = get_input("day01test.txt")

    distance = get_distance(list1, list2)

    assert distance == 11, "Distance test failed"

    similarity = get_similarity(list1, list2)

    assert similarity == 31, "Similarity test failed"

    print("Tests passed")


if __name__ == "__main__":

    tests()

    main()
