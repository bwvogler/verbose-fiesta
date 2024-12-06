import numpy as np

with open("aoc2024/data/day2.txt", encoding="utf-8") as f:
    data = [[int(x) for x in line.split()] for line in f.read().splitlines()]


def _safe(row):
    diff = np.diff(np.array(row))
    return np.all((-4 < diff) & (diff < 0)) or np.all((4 > diff) & (diff > 0))


len([row for row in data if _safe(row)])


def _semi_safe(row):
    return any(
        _safe(dampened_row)
        for dampened_row in [row[:i] + row[i + 1 :] for i in range(len(row))]
    )


len([row for row in data if _semi_safe(row)])
