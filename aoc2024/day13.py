"""Button A: X+11, Y+73
Button B: X+65, Y+17
Prize: X=18133, Y=4639
"""

import re
import numpy as np

with open("aoc2024/data/day13.txt") as f:
    blocks = f.read().split("\n\n")

data = [
    {
        key: np.array(
            [int(x) for x in re.match(r"X[\+=](\d+), Y[\+=](\d+)", value).groups()]
        )
        for key, value in (line.split(": ") for line in block.splitlines())
    }
    for block in blocks
]


def solution(a, b, prize) -> int | None:
    x2 = (a[0] * prize[1] - a[1] * prize[0]) / (a[0] * b[1] - a[1] * b[0])
    x1 = (prize[0] - b[0] * x2) / a[0]
    if x1.is_integer() and x2.is_integer():
        if x1 >= 0 and x2 >= 0:
            return int(3 * x1 + x2)
    return None


results = [
    solution(machine["Button A"], machine["Button B"], machine["Prize"])
    for machine in data
]
sum(result for result in results if result is not None)

# Part 2

data = [
    {
        key: (value if key != "Prize" else value + 10000000000000)
        for key, value in machine.items()
    }
    for machine in data
]


results = [
    solution(machine["Button A"], machine["Button B"], machine["Prize"])
    for machine in data
]
sum(result for result in results if result is not None)
