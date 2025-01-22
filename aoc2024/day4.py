import regex as re
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

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


# Part 2
# Get the sliding windows
window_view_down = sliding_window_view(data, (3, 3))
window_view_up = sliding_window_view(data[::-1], (3, 3))[::-1]


# Function to get the diagonals
def _get_diagonals(arr: np.ndarray) -> np.ndarray:
    rows, cols, _, _ = arr.shape
    return np.array(
        [["".join(arr[i, j].diagonal()) for j in range(cols)] for i in range(rows)],
        dtype=str,
    )


diag_up = _get_diagonals(window_view_up)
diag_down = _get_diagonals(window_view_down)


def _is_mas(x):
    if x == "MAS":
        return True
    if x == "SAM":
        return True
    return False


is_mas = np.vectorize(_is_mas)

# Apply the function to each element of the array
(is_mas(diag_down) & is_mas(diag_up)).sum()
