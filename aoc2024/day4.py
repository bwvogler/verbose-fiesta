import regex as re
import numpy as np

with open("aoc2024/data/day4.txt", encoding="utf-8") as f:
    data = np.array([list(line.strip()) for line in f.readlines()])

across = ["".join(row) for row in data]
down = ["".join(row) for row in data.T]

diagonal_down = [
    "".join(data.diagonal(i)) for i in range(data.shape[1] - 1, -data.shape[0], -1)
]
diagonal_up = [
    "".join(data[::-1].diagonal(i))
    for i in range(data.shape[1] - 1, -data.shape[0], -1)
]

sum(
    len(re.findall(r"XMAS|SAMX", line, overlapped=True))
    for line in across + down + diagonal_down + diagonal_up
)


rows, cols = data.shape

# Diagonal from Top-Left to Bottom-Right
diagonal_down = np.array(
    [
        [
            "".join([data[i - 1, j - 1], data[i, j], data[i + 1, j + 1]])
            for j in range(1, cols - 1)
        ]
        for i in range(1, rows - 1)
    ],
    dtype=str,
)

diagonal_up = np.array(
    [
        [
            "".join([data[i - 1, j + 1], data[i, j], data[i + 1, j - 1]])
            for j in range(1, cols - 1)
        ]
        for i in range(1, rows - 1)
    ],
    dtype=str,
)

across = np.array(
    [
        ["".join(data[i, j - 1 : j + 2]) for j in range(1, cols - 1)]
        for i in range(1, rows - 1)
    ],
    dtype=str,
)

down = np.array(
    [
        ["".join(data[i - 1 : i + 2, j].flatten()) for j in range(1, cols - 1)]
        for i in range(1, rows - 1)
    ],
    dtype=str,
)
