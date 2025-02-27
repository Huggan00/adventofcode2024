import time


def get_input(filename):

    with open("inputs/" + filename, "r") as input:
        pass


def main():

    start = time.time()

    end = time.time()
    duration = end - start
    print(f"Executed in {duration} seconds")


def tests():

    print("Tests passed")


if __name__ == "__main__":

    tests()

    main()
