import time


def get_input():
    with open("day9/input.txt", "r") as input:
        line = input.readline()

        blocks = []

        for i, char in enumerate(line):

            if i % 2 == 0:
                blocks.extend([i // 2 for _ in range(int(char))])
            else:
                blocks.extend([-1 for _ in range(int(char))])

        return blocks


def move_blocks(blocks):

    start = 0
    end = len(blocks) - 1

    while start < end:
        while start < end and blocks[start] >= 0:
            start += 1
        while start < end and blocks[end] < 0:
            end -= 1
        blocks[start], blocks[end] = blocks[end], blocks[start]


def move_files(blocks):
    empty_start = 0
    file_end = len(blocks)
    file_start = file_end

    while True:
        while blocks[file_end - 1] < 0:
            file_end -= 1
        file_id = blocks[file_end - 1]
        file_start = file_end
        while file_start > 0 and blocks[file_start - 1] == file_id:
            file_start -= 1
        if file_start == 0:
            break
        file_size = file_end - file_start

        while True:
            while empty_start < file_start and blocks[empty_start] >= 0:
                empty_start += 1
            empty_end = empty_start
            while blocks[empty_end] < 0:
                empty_end += 1
            empty_size = empty_end - empty_start

            if empty_start >= file_start:
                empty_start = 0
                file_end = file_start
                break
            elif empty_size >= file_size:
                blocks[empty_start : empty_start + file_size] = blocks[
                    file_start:file_end
                ]
                blocks[file_start:file_end] = [-1 for _ in range(file_size)]
                empty_start = 0
                file_end = file_start
                break
            else:
                empty_start = empty_end


def checksum(blocks):

    result = 0

    for i, id in enumerate(blocks):
        if id >= 0:
            result += i * id

    return result


if __name__ == "__main__":
    start = time.time()
    blocks = get_input()
    blocks_copy = blocks.copy()
    end = time.time()
    duration = end - start
    print(f"Reading input took {duration} seconds")

    start = time.time()

    move_blocks(blocks)

    result = checksum(blocks)

    end = time.time()
    duration = end - start
    print(
        f"The checksum of rearranged blocks is: {result}, executed in {duration} seconds"
    )

    blocks = blocks_copy

    start = time.time()

    move_files(blocks)

    result = checksum(blocks)

    end = time.time()
    duration = end - start
    print(
        f"The checksum of rearranged files is: {result}, executed in {duration} seconds"
    )
