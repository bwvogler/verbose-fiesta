with open("aoc2024/data/day12.txt", encoding="utf-8") as f:
  data = np.array([list(line.strip()) for line in f.readlines()])

class GardenRegion():
  def __init__(self, label: str, locations: set[tuple[int, int]])
    self.locations = locations

  def is_same(self, other_region: GardenRegion) -> bool:
    if other_region.label != self.label:
      return False
    if any(
      other_region.location == tuple(np.add(self.location, direction))
      for direction in self._directions
    )

  def add_locations(locations: list[tuple(int, int) | np.ndarray | GardenRegion]):
    pass

  @property
  def area(self) -> int:
    return self.locations.shape[0]

  @property
  def perimeter(self) -> int:
    return sum(
      location + direction not in self.locations
      for direction in self._directions
      for location in self.locations
    )

garden = [
  GardenRegion(data[i, j] for i, j in list(np.ndindex(data.shape))
]

for region in garden:
  adjoining_regions = [
    other_region
    for other_region in garden
    if other_region.is_same(region)
  ]
  region.add_locations(

