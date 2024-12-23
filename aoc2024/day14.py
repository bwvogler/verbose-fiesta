"p=40,73 v=-96,64"
import re
import numpy as np

shape = (101, 103)
# shape = (11, 7)
with open("aoc2024/data/day14.txt", encoding="utf-8") as f:
    #     f="""p=0,4 v=3,-3
    # p=6,3 v=-1,-3
    # p=10,3 v=-1,2
    # p=2,0 v=2,-1
    # p=0,0 v=1,3
    # p=3,0 v=-2,-2
    # p=7,6 v=-1,-3
    # p=3,0 v=-1,-2
    # p=9,3 v=2,3
    # p=7,3 v=-1,2
    # p=2,4 v=2,-3
    # p=9,5 v=-3,-3"""
    data = [
        [np.array(list(map(int, pv.split(",")))) for pv in match.groups()]
        for line in f
        # for line in f.splitlines()
        if (match := re.search(r"p=(-?\d+,-?\d+) v=(-?\d+,-?\d+)", line))
    ]


def get_positions(
    t: int, data: list[list[np.ndarray]] = data, shape: tuple[int, int] = shape
) -> np.ndarray:
    return np.array([(p + t * v) % shape for p, v in data])


positions = get_positions(100)

np.array(
    [
        positions[
            (left < positions[:, 0])
            & (positions[:, 0] < right)
            & (top < positions[:, 1])
            & (positions[:, 1] < bottom)
        ].shape[0]
        for left, right, top, bottom in [
            (-1, shape[0] // 2, -1, shape[1] // 2),
            (shape[0] // 2, shape[0], shape[1] // 2, shape[1]),
            (shape[0] // 2, shape[0], -1, shape[1] // 2),
            (-1, shape[0] // 2, shape[1] // 2, shape[1]),
        ]
    ]
).prod()


def christmas_tree(arr: np.ndarray, shape: tuple[int, int] = shape) -> bool:
    "Find if there is a christmas tree in the array of positions, so that there is a triangle of the positions."
    # left side is from bottom left (shape[1], 0) to center middle positions of shape (0, shape[1]//2)
    left_side_of_tree = [[(shape[1] - 2 * i, 0 + i)] for i in range(shape[0] // 2)]
    # right side is from center middle positions of shape (0, shape[1]//2) to bottom right (shape[0], shape[1])
    right_side_of_tree = [
        [(0 + 2 * i, shape[1] // 2 + i)] for i in range(shape[0] // 2)
    ]
    # bottom of tree is from bottom left (shape[0], 0) to bottom right (shape[0], shape[1])
    bottom_of_tree = [[(shape[0], i)] for i in range(shape[1])]
    return all(
        np.all(np.isin(pos, arr))
        for pos in left_side_of_tree + right_side_of_tree + bottom_of_tree
    )


t = 0
while True:
    positions = get_positions(t, positions)
    if christmas_tree(positions):
        break
    t += 1
