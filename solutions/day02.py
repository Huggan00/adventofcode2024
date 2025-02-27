import time


def get_input(filename):
    list = []

    with open("inputs/" + filename, "r") as input:
        for line in input:
            values = line.split()
            values = [int(value) for value in values]
            list.append(values)

    return list


def is_safe(list):
    if list[0] < list[1]:
        increasing = True
    else:
        increasing = False

    for i in range(len(list) - 1):
        if list[i] == list[i + 1]:
            return False
        if abs(list[i] - list[i + 1]) > 3:
            return False
        if list[i] < list[i + 1] and not increasing:
            return False
        elif list[i] > list[i + 1] and increasing:
            return False

    return True


def num_safe_reports(list):
    num_safe_reports = 0

    for report in list:
        if is_safe(report):
            num_safe_reports += 1
    return num_safe_reports


def num_safeish_reports(list):
    num_safe_reports = 0

    for report in list:
        for i in range(len(report)):
            dampened_report = [report[k] for k in range(len(report)) if k != i]
            if is_safe(dampened_report):
                num_safe_reports += 1
                break
    return num_safe_reports


def main():
    start = time.time()
    list = get_input("day02.txt")

    safe_reports = num_safe_reports(list)
    print(f"Number of safe reports: {safe_reports}")

    safeish_reports = num_safeish_reports(list)
    print(f"Number of safe-ish reports: {safeish_reports}")

    end = time.time()
    duration = end - start

    print(f"executed in {duration:.3f} seconds")


def tests():

    list = get_input("day02test.txt")

    safe_reports = num_safe_reports(list)
    assert safe_reports == 2

    safeish_reports = num_safeish_reports(list)
    assert safeish_reports == 4

    print("Tests passed")


if __name__ == "__main__":

    tests()

    main()
