import re
import numpy as np

with open("aoc2024/data/day3.txt", encoding="utf-8") as f:
    data = f.read()

np.array(re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", data)).astype(int).prod(axis=1).sum()

enabled = re.findall(r"(?:^|do\(\))(?:(?!don\'t\(\)).)*", data.replace("\n", ""))

sum(
    np.array(re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", e))
    .astype(int)
    .prod(axis=1)
    .sum()
    for e in enabled
)
