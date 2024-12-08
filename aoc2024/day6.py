import numpy as np
from itertools import cycle

with open("aoc2024/data/day6.txt", encoding="utf-8") as f:
    data = np.array([list(line.strip()) for line in f.readlines()])


explored = np.zeros_like(data, dtype=bool)
start = np.where(data == "^")

directions = cycle([(-1, 0), (0, 1), (1, 0), (0, -1)])
explored[start] = True
while True:
    direction = next(directions)

    new_position = (start[0][0] + direction[0], start[1][0] + direction[1])

    if (
        0 <= new_position[0] < data.shape[0]
        and 0 <= new_position[1] < data.shape[1]
        and not explored[new_position]
    ):
        explored[new_position] = True
        start = (np.array([new_position[0]]), np.array([new_position[1]]))
