import numpy as np

with open("aoc2024/data/day11.txt", encoding="utf-8") as f:
    stones: np.ndarray = np.array(f.read().strip().split(" "), dtype=str)
# stones = np.array("125 17".split(" "), dtype=str)


# If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
# If the stone is engraved with a number that has an even number of digits, it is replaced by two stones. The left half
# of the digits are engraved on the new left stone, and the right half of the digits are engraved on the new right
# stone. (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
# If none of the other rules apply, the stone is replaced by a new stone; the old stone's number multiplied by 2024 is
# engraved on the new stone.


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
