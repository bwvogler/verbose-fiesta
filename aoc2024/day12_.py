class GardenRegion():
  def __init__(self, label: str, locations: np.ndarray)
    self.locations = locations

  def is_adjoining(self, other_region: GardenRegion):
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