with open("aoc2024/data/day12.txt", encoding="utf-8") as f:
  data = np.array([list(line.strip()) for line in f.readlines()])

class GardenRegion():
  def __init__(self, label: str, locations: set[np.ndarray])
    self.locations = locations

  def _directions(self) -> list[np.ndarray]:
    return [
      np.array(x, y)
      for x, y in [(1, 0), (0, -1), (-1,0),(0,1)]
    ]

  def is_same(self, other_region: GardenRegion) -> bool:
    if other_region.label != self.label:
      return False
    if any(
      other_region.location == self.location + direction
      for direction in self._directions
    )

  def merge(self, regions: GardenRegion | list[GardenRegion]):
    if isinstance(regions, GardenRegion):
      regions = [regions]
    for region in regions:
      self.locations.add(region.location)

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

