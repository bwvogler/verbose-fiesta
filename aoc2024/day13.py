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

hunderd = np.array([(100)])
results = [
    min(
        (
            3 * a_count + b_count
            # tuple(a_count * a + b_count * b)
            for a_count in range(
                np.hstack([(machine["Prize"] // machine["Button A"]), hunderd]).min()
            )
            for b_count in range((machine["Prize"] // machine["Button B"]).min())
            if tuple(a_count * machine["Button A"] + b_count * machine["Button B"])
            == tuple(machine["Prize"])
        ),
        default=None,
    )
    for machine in data
]
sum(result for result in results if result is not None)
