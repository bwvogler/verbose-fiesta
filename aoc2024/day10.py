import numpy as np

with open("aoc2024/data/day10.txt", encoding="utf-8") as f:
    data = np.array([list(line.strip()) for line in f.readlines()], dtype=int)

trailheads = np.array(np.where(data == 0)).T

directions = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])


def in_bounds(x: int, y: int) -> bool:
    """Check if the coordinates are within the bounds of the data array"""
    return 0 <= x < data.shape[0] and 0 <= y < data.shape[1]


def get_trail(x: int, y: int) -> list[tuple[int, int]]:
    """Get the score of the hiking trail"""
    if data[x, y] == 9:
        return [(x, y)]
    return [
        a
        for b in [
            get_trail(x + dx, y + dy)
            for dx, dy in directions
            if in_bounds(x + dx, y + dy) and (data[x + dx, y + dy] == data[x, y] + 1)
        ]
        for a in b
    ]


sum(len(set(get_trail(x, y))) for x, y in trailheads)

sum(len(get_trail(x, y)) for x, y in trailheads)
