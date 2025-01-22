import numpy as np

with open("aoc2024/data/day1.txt", encoding="utf-8") as f:
    data = np.array([[int(x) for x in line.split()] for line in f.read().splitlines()])

# sort each column independently
data = np.sort(data, axis=0)

# calculate the absolute difference of each row
diff = np.abs(data[:, 0] - data[:, -1])

# calculate the sum of the differences
print(diff.sum())

# count how many times each number from the first column appears in the second column
locations, counts = np.unique(
    # just the items in column two that are in column 1, using only the val
    data[:, -1][np.isin(data[:, -1], data[:, 0])],
    return_counts=True,
)

(locations * counts).sum()
