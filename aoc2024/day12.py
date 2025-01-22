import numpy as np
from scipy.ndimage import label

with open("aoc2024/data/day12.txt", encoding="utf-8") as f:
    data = np.array([list(line.strip()) for line in f.readlines()])


def label_contiguous_regions(array, connectivity=1):
    structure = (
        np.ones((3, 3), dtype=int)
        if connectivity == 2
        else np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=int)
    )
    labeled_array, num_features = label(array, structure)
    return labeled_array, num_features


def list_contiguous_regions(array) -> list[np.ndarray]:
    labeled_array, num_features = label_contiguous_regions(array)
    regions = [1 * (labeled_array == label) for label in range(1, num_features + 1)]
    return regions


def perimeter_of_contiguous_region(region: np.ndarray) -> int:
    region = np.pad(region, 1)
    vertical_edges = np.sum(region[1:, :] != region[:-1, :])
    horizontal_edges = np.sum(region[:, 1:] != region[:, :-1])
    return vertical_edges + horizontal_edges


gardens = [1 * (data == plot_label) for plot_label in np.unique(data)]

contiguous_regions = [
    x for y in [list_contiguous_regions(garden) for garden in gardens] for x in y
]

perimeters = [perimeter_of_contiguous_region(region) for region in contiguous_regions]
areas = [np.sum(region) for region in contiguous_regions]
sum(perimeter * area for perimeter, area in zip(perimeters, areas))

# Part 2


def sections_of_perimeter(region: np.ndarray) -> int:
    region = np.pad(region, 1)
    top_edges = np.diff(1 * (region[1:, :] > region[:-1, :]), axis=1).sum()
    left_edges = np.diff(region[:, 1:] > region[:, :-1], axis=0).sum()

    bottom_edges = np.diff(1 * (region[1:, :] < region[:-1, :]), axis=1).sum()
    right_edges = np.diff(region[:, 1:] < region[:, :-1], axis=0).sum()
    return top_edges + left_edges + bottom_edges + right_edges


sections = [sections_of_perimeter(region) for region in contiguous_regions]
sum(section * area for section, area in zip(sections, areas))
