from tqdm import tqdm
import numpy as np

with open("aoc2024/data/day11.txt", encoding="utf-8") as f:
   stones = np.array(f.read().strip().split(" "))

# If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
# If the stone is engraved with a number that has an even number of digits, it is replaced by two stones. The left half of the digits are engraved on the new left stone, and the right half of the digits are engraved on the new right stone. (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
# If none of the other rules apply, the stone is replaced by a new stone; the old stone's number multiplied by 2024 is engraved on the new stone.

def update_stone(stone: int) -> tuple[int, int]:
   if stone == 0:
      return (1, -1)
   if (string_len:=len(stone_string:=str(stone))) % 2 == 0:
      return (
         int(stone_string[:string_len//2]),
         int(stone_string[string_len//2:]),
      )
   return (2024*stone, -1)

update_stones = np.vectorize(update_stone).flatten()

for look in tqdm(range(25)):
   stones = update_stones(stones)
