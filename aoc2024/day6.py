from itertools import cycle

import numpy as np

with open("aoc2024/data/day6.txt", encoding="utf-8") as f:
    data = np.array([list(line.strip()) for line in f.readlines()])

# make an array of tuple(0, 0) with the same shape
explored = np.empty_like(data, dtype=tuple)
explored.fill((0, 0))
obstruction_options = np.zeros_like(data, dtype=bool)
position = np.array(np.where(data == "^")).flatten()


class Directions:
    def __init__(self, direction=None):
        self.directions = cycle(np.array(x) for x in [(-1, 0), (0, 1), (1, 0), (0, -1)])
        self.direction = next(self.directions)
        if direction is not None:
            while tuple(self.direction) != tuple(direction):
                self.turn()

    def __next__(self):
        self.turn()
        return self.direction

    def turn(self):
        self.direction = next(self.directions)

    def copy(self):
        new_directions = Directions()
        while tuple(new_directions.direction) != tuple(self.direction):
            new_directions.turn()
        return new_directions


directions = Directions()
direction = next(directions)
rows, columns = np.indices(data.shape)


def _causes_loop(position, direction, explored):
    directions_copy = Directions(direction)
    new_direction = next(directions_copy)
    row, column = position
    obstructions_in_new_path = np.array(
        np.where(
            (data == "#")
            & (np.sign(rows - row) == new_direction[0])
            & (np.sign(columns - column) == new_direction[1])
        )
    ).T
    if not obstructions_in_new_path.size:
        return False
    next_obstruction = list(np.sort(obstructions_in_new_path, axis=0))[
        :: [x for x in new_direction if x != 0][0]
    ][0]
    if tuple(explored[tuple(next_obstruction - new_direction)]) == tuple(
        next(directions_copy)
    ):
        return True
    return False


while (0 <= position[0] < data.shape[0]) and (0 <= position[1] < data.shape[1]):
    explored[tuple(position)] = direction
    # if the next location is an obstruction, then turn until it's not
    while (
        (0 <= position[0] + direction[0] < data.shape[0])
        and (0 <= position[1] + direction[1] < data.shape[1])
        and data[tuple(position + direction)] == "#"
    ):
        direction = next(directions)
    # if the next step has been visited, then placing an obstruction beyond it would cause a loop
    if (
        (0 <= position[0] + direction[0] < data.shape[0])
        and (0 <= position[1] + direction[1] < data.shape[1])
        and _causes_loop(position, direction, explored)
    ):
        obstruction_options[tuple(position + direction)] = True
    position += direction

np.sum(np.vectorize(lambda x: abs(sum(x)))(explored))

np.sum(obstruction_options)
