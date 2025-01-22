import numpy as np

with open("aoc2024/data/day8.txt", encoding="utf-8") as f:
    data = np.array([list(line.strip()) for line in f.readlines()])

alphanumerics = (
    [str(i) for i in range(10)]
    + [chr(i) for i in range(65, 91)]
    + [chr(i) for i in range(97, 123)]
)


def in_bounds(x: int, y: int) -> bool:
    """Check if the coordinates are within the bounds of the data array"""
    return 0 <= x < data.shape[0] and 0 <= y < data.shape[1]


alphanumeric = next(iter(alphanumerics))
indices = np.array(np.where(data == alphanumeric)).T
antinodes = [
    a
    for alphanumeric in alphanumerics
    for antenna_x, antenna_y in [
        (x, y)
        for x, row in enumerate(data)
        for y, value in enumerate(row)
        if value == alphanumeric
    ]
    for x, y in [
        (x, y)
        for x, row in enumerate(data)
        for y, value in enumerate(row)
        if value == alphanumeric
    ]
    if not (x == antenna_x and y == antenna_y)
    for a in [
        (antenna_x - (x - antenna_x), antenna_y - (y - antenna_y)),
        (x + (x - antenna_x), y + (y - antenna_y)),
    ]
    if in_bounds(*a)
]

len(set(tuple(a) for a in antinodes))


def get_antinodes(
    antenna1: tuple[int, int], antenna2: tuple[int, int]
) -> list[tuple[int, int]]:
    def on_antinode_line(x: int, y: int) -> bool:
        return (x - antenna1[0]) * (y - antenna2[1]) == (x - antenna2[0]) * (
            y - antenna1[1]
        )

    # return the coordinates that are on the line connecting the antennas
    return [(x, y) for x, y in np.ndindex(data.shape) if on_antinode_line(x, y)]


antinodes = [
    a
    for alphanumeric in alphanumerics
    for antenna1 in [
        (x, y)
        for x, row in enumerate(data)
        for y, value in enumerate(row)
        if value == alphanumeric
    ]
    for antenna2 in [
        (x, y)
        for x, row in enumerate(data)
        for y, value in enumerate(row)
        if value == alphanumeric
    ]
    if antenna1 != antenna2
    for a in get_antinodes(antenna1, antenna2)
]

len(set(tuple(a) for a in antinodes))
