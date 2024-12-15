with open("aoc2024/data/day12.txt", encoding="utf-8") as f:
  data = np.array([list(line.strip()) for line in f.readlines()])

class GardenRegion():
  def __init__(self, label: str, locations: set[tuple[int, int]])
    self.locations = locations

  def is_adjoining(self, other_region: GardenRegion):
    pass

  def add_location(location: tuple(int, int) | np.ndarray | GardenRegion):
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

