"parse a gxii file"
import re
import string

with open("labchip/data/Gold Test.gxd", "rb") as f:
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
