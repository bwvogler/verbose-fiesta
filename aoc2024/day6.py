from itertools import cycle

import numpy as np

with open("aoc2024/data/day6.txt", encoding="utf-8") as f:
    data = np.array([list(line.strip()) for line in f.readlines()])


class Directions:
    """A class to cycle through the directions of the compass"""

    def __init__(self, direction=None):
        self.directions = cycle(np.array(x) for x in [(-1, 0), (0, 1), (1, 0), (0, -1)])
        self.direction = next(self.directions)
        if direction is not None:
            if isinstance(direction, tuple):
                direction = np.array(direction)
            while tuple(self.direction) != tuple(direction):
                self.turn()

    def __next__(self):
        self.turn()
        return self.direction

    def turn(self):
        """Turn the direction clockwise"""
        self.direction = next(self.directions)

    def copy(self):
        """Return a new Directions object with the same direction"""
        new_directions = Directions()
        while tuple(new_directions.direction) != tuple(self.direction):
            new_directions.turn()
        return new_directions


def _is_on_map(position: np.ndarray, map_data: np.ndarray = data) -> bool:
    if (0 <= position[0] < map_data.shape[0]) and (
        0 <= position[1] < map_data.shape[1]
    ):
        return True
    return False


def explore(map_data: np.ndarray) -> np.ndarray:
    """Explore a map, returning the direction of travel at each location"""
    # make an array of tuple(0, 0) with the same shape
    explored_directions = np.empty_like(map_data, dtype=tuple)
    explored_directions.fill((0, 0))
    position = np.array(np.where(map_data == "^")).flatten()
    directions = Directions()
    while _is_on_map(position):
        # if we've been here before, going the same direction, then we've found a loop
        if tuple(explored_directions[tuple(position)]) == tuple(directions.direction):
            raise ValueError("Loop found")
        explored_directions[tuple(position)] = directions.direction
        # if the next location is an obstruction, then turn until it's not
        while (
            _is_on_map(position + directions.direction)
            and map_data[tuple(position + directions.direction)] == "#"
        ):
            directions.turn()
        position += directions.direction
    return explored_directions


explored = explore(data)

np.sum(np.vectorize(lambda x: abs(sum(x)))(explored))


def causes_loop(map_data: np.ndarray) -> bool:
    """Return True if the map causes a loop, False otherwise"""
    try:
        _ = explore(map_data)
    except ValueError:
        return True
    return False


path_positions = [
    (i, j)
    for i, j in np.ndindex(data.shape)
    if tuple(explored[i, j]) != (0, 0) and data[i, j] == "."
]
data_copies = [data.copy() for _ in path_positions]
for (i, j), data_copy in zip(path_positions, data_copies):
    data_copy[i, j] = "#"

sum(causes_loop(data_copy) for data_copy in data_copies)
