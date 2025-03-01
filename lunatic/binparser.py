# parse the file in "lunatic/data/2025-01-15_161155_401155_LUNA.bin"
import re
import string

with open("lunatic/data/2025-01-15_161155_401155_LUNA.bin", "rb") as f:
    data = f.read()
lines = [line.strip(b"\x00") for line in data.splitlines()]
chunks = [re.split(b"\x00+", line) for line in lines]


def parse_chunk(chunk: bytes, toint: bool = False):
    if 0 < len(chunk) == int(chunk[0]) + 1 and all(
        x in string.printable.encode("utf-8") for x in chunk
    ):
        return chunk[1:].decode("utf-8")
    if len(chunk) > 1 and all(x in string.printable.encode("utf-8") for x in chunk):
        return chunk.decode("utf-8")
    if len(chunk) > 1 and chunk[-1] in b"\x00\x01":
        return (parse_chunk(chunk[:-1]), bool(chunk[-1]))
    if toint:
        return int.from_bytes(chunk)
    return chunk

def parse_single(chunklet: str):
    pattern = r"(?P<attribute_string>.+) = \"(?P<value_size>[0-9]+)?(?P<unit>[A-Z]+)?(?P<status>[A-Z]+)?"
    match_obj = re.match(r"(P?)", chunklet)

parsed = [[parse_chunk(chunk, toint=True) for chunk in chunkset] for chunkset in chunks]
[line for line in parsed if len(line) == 1]
line_lengths = [len(line) for line in parsed]
#plot histogram of line lengths
import matplotlib.pyplot as plt
plt.hist(line_lengths, bins=range(0, 50))
plt.show()