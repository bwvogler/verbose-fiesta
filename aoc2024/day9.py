import numpy as np

with open("aoc2024/data/day9.txt", encoding="utf-8") as f:
    data = f.read()

# data = "2333133121414131402"


def build_file_system(data: str) -> np.ndarray:
    file_array = -np.ones(sum(int(x) for x in list(data.strip())), dtype=np.int64)
    fileno = 0
    i = 0
    is_file = True
    for x in list(data.strip()):
        if is_file:
            file_array[i : i + int(x)] = fileno
            fileno += 1
        i += int(x)
        is_file = not is_file
    return file_array


file_array = build_file_system(data)


while (spaces := np.where(file_array == -1)[0])[0] < (
    files := np.where(file_array != -1)[0]
)[-1]:
    file_array[spaces[0]] = file_array[files[-1]]
    file_array[files[-1]] = -1

non_empty_files = file_array[file_array != -1]
(non_empty_files * np.arange(len(non_empty_files))).sum()


# Part 2

file_array = build_file_system(data)


def get_spaces(file_array: np.ndarray) -> np.ndarray:
    """Get the start and end of the spaces in the file system"""
    borders = np.where(np.diff(file_array == -1))[0] + 1
    if len(borders) % 2 == 0:
        return borders.reshape(-1, 2)
    return np.hstack([borders, np.array([file_array.size])]).reshape(-1, 2)


file_chunks = np.array(
    [
        (x[0], x[-1] + 1)
        for x in [
            np.where(file_array == x)[0] for x in np.unique(file_array) if x != -1
        ]
    ]
)[::-1]
for file_start, file_end in file_chunks:
    spaces = get_spaces(file_array)
    if viable_spaces := [
        space
        for space in spaces
        if space[1] - space[0] >= file_end - file_start and space[0] <= file_start
    ]:
        space_start = viable_spaces[0][0]
        file_array[space_start : space_start + file_end - file_start] = file_array[
            file_start:file_end
        ]
        file_array[file_start:file_end] = -1

# now there are spaces remaining, so have to number the files without first removing the spaces
(file_array * np.arange(file_array.size))[file_array != -1].sum()
