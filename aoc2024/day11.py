import numpy as np
from tqdm import tqdm
from collections import defaultdict


with open("aoc2024/data/day11.txt", encoding="utf-8") as f:
    stones: np.ndarray = np.array(f.read().strip().split(" "), dtype=str)
# stones = np.array("125 17".split(" "), dtype=str)


def update_stone(stone: str) -> tuple[str, str]:
    if int(stone) == 0:
        return ("1", "-1")
    if (string_len := len(stone)) % 2 == 0:
        return (
            stone[: string_len // 2],
            str(int(stone[string_len // 2 :])),
        )
    return (str(2024 * int(stone)), "-1")


update_stones = np.vectorize(update_stone)

for look in range(25):
    stones = np.array(update_stones(stones)).T.flatten()
    stones = stones[stones != "-1"]
    print(" ".join(stones))
stones.size

# Part 2

# Initialize stone counts
stone_counts: dict[str, int] = defaultdict(int)
for stone in stones:
    stone_counts[stone] += 1


def update_stone_counts(stone_counts):
    new_counts = defaultdict(int)
    for stone, count in stone_counts.items():
        num = int(stone)
        if num == 0:
            new_counts["1"] += count
        elif len(stone) % 2 == 0:
            left = stone[: len(stone) // 2].lstrip("0") or "0"
            right = stone[len(stone) // 2 :].lstrip("0") or "0"
            new_counts[left] += count
            new_counts[right] += count
        else:
            new_stone = str(2024 * num)
            new_counts[new_stone] += count
    return new_counts


for _ in tqdm(range(75)):
    stone_counts = update_stone_counts(stone_counts)
sum(stone_counts.values())
