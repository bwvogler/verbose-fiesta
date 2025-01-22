from __future__ import annotations
import numpy as np

with open("aoc2024/data/day12.txt", encoding="utf-8") as f:
    data = np.array([list(line.strip()) for line in f.readlines()])


class GardenRegion:
    def __init__(self, label: str, locations: list[np.ndarray]):
        self.label = label
        self.locations: set[tuple[int, int]] = set((x, y) for x, y in locations)

    @property
    def location_array(self) -> np.ndarray:
        return np.array(list(self.locations))

    @property
    def _directions(self) -> list[np.ndarray]:
        return [np.array((x, y)) for x, y in [(1, 0), (0, -1), (-1, 0), (0, 1)]]

    def can_merge(self, other_region: GardenRegion) -> bool:
        if other_region.label != self.label:
            return False
        return any(
            tuple(location) in self.adjacent_locations
            for location in other_region.location_array
        )

    def merge(self, regions: GardenRegion | list[GardenRegion]):
        """
        Merge the current region with one or more other regions.

        Args:
            regions (GardenRegion | list[GardenRegion]): The region(s) to merge with.
        """
        if isinstance(regions, GardenRegion):
            regions = [regions]
        for reg in regions:
            self.locations.update(reg.locations)

    @property
    def adjacent_locations(self) -> set[np.ndarray]:
        adjacent_locations_array = np.vstack(
            [self.location_array + direction for direction in self._directions]
        )
        return set(map(tuple, adjacent_locations_array))

    @property
    def area(self) -> int:
        return len(self.locations)

    @property
    def perimeter(self) -> int:
        return sum(
            adjacent_location not in self.locations
            for adjacent_location in self.adjacent_locations
        )


garden = [
    GardenRegion(data[i, j], [np.array((i, j))])
    for i, j in list(np.ndindex(data.shape))
]

while any(
    region.can_merge(other_region) for region in garden for other_region in garden
):
    for region in garden:
        regions_can_merge = [
            other_region for other_region in garden if region.can_merge(other_region)
        ]
        if regions_can_merge:
            region.merge(regions_can_merge)
            garden = [g for g in garden if g not in regions_can_merge]
            print(len(garden))

list(region.perimeter * region.area for region in garden)
garden[0].locations
