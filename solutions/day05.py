import time


def get_input(filename):
    pages = {}
    updates = []

    with open("inputs/" + filename, "r") as input:
        for line in input:
            if "|" in line:
                numbers = line.split("|")
                first = int(numbers[0])
                second = int(numbers[1])

                if first not in pages:
                    pages[first] = Page(first)

                pages[first].after.add(second)

            elif "," in line:
                numbers = line.split(",")
                numbers = [int(number) for number in numbers]

                update = []
                for number in numbers:
                    if number not in pages:
                        pages[number] = Page(number)
                    update.append(pages[number])

                updates.append(update)

    return updates


class Page:

    def __init__(self, number):
        self.number = number
        self.after = set()

    def __lt__(self, other):
        return other.number in self.after

    def __hash__(self):
        return hash(self.number)

    def __str__(self):
        return f"Page {self.number}"


def is_valid(update):

    for i, page in enumerate(update):
        previous_pages = update[:i]
        previous_page_numbers = {page.number for page in previous_pages}
        if page.after.intersection(previous_page_numbers):
            return False

    return True


def valid_updates(updates):
    sum = 0
    for update in updates:

        if is_valid(update):
            middle_page = update[len(update) // 2].number
            sum += middle_page

    return sum


def invalid_updates(updates):
    sum = 0
    for update in updates:

        if not is_valid(update):
            sorted_update = sorted(update)
            middle_page = sorted_update[len(sorted_update) // 2].number
            sum += middle_page

    return sum


def main():

    start = time.time()

    updates = get_input("day05.txt")

    sum = valid_updates(updates)
    print(f"The sum of valid updates is:   {sum}")

    sum = invalid_updates(updates)
    print(f"The sum of invalid updates is: {sum}")

    end = time.time()
    duration = end - start
    print(f"Executed in {duration} seconds")


def tests():

    updates = get_input("day05test.txt")

    sum = valid_updates(updates)
    assert sum == 143

    sum = invalid_updates(updates)
    assert sum == 123

    print("Tests passed")


if __name__ == "__main__":

    tests()

    main()
