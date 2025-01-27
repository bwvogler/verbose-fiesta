# parse the file in "lunatic/data/2025-01-15_161155_401155_LUNA.bin"

with open("lunatic/data/2025-01-15_161155_401155_LUNA.bin", "rb") as f:
    data = f.read()
lines = data.splitlines()

data_iter = iter(data[:1000])
data_string = ""
try:
    while True:
        datum = next(data_iter)
        if datum == 0:
            continue
        string_length = datum
        data_string += "".join([chr(next(data_iter)) for _ in range(string_length)])
except StopIteration:
    print("Reached the end of data while processing.")

print(data_string)
len(data.splitlines())
