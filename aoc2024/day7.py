from typing import Iterator
from itertools import product

with open("aoc2024/data/day7.txt", encoding="utf-8") as f:
    data = [
        [
            (
                int(line.strip().split(":")[0]),
                [int(x) for x in line.strip().split(":")[-1].strip().split(" ")],
            )
        ][0]
        for line in f.readlines()
    ]


def multiply(a, b):
    return a * b


def add(a, b):
    return a + b


def get_possible_results(test_numbers: list[int]) -> Iterator:
    possible_functions = product([multiply, add], repeat=len(test_numbers) - 1)
    for function_set in possible_functions:
        result = test_numbers[0]
        for i, fun in enumerate(function_set):
            result = fun(result, test_numbers[i + 1])
        yield result


sum(
    test_value
    for test_value, test_numbers in data
    if any(
        test_result == test_value for test_result in get_possible_results(test_numbers)
    )
)


def concatenate(a, b):
    return int(str(a) + str(b))


def get_more_possible_results(test_numbers: list[int]) -> Iterator:
    possible_functions = product(
        [multiply, add, concatenate], repeat=len(test_numbers) - 1
    )
    for function_set in possible_functions:
        result = test_numbers[0]
        for i, fun in enumerate(function_set):
            result = fun(result, test_numbers[i + 1])
        yield result


sum(
    test_value
    for test_value, test_numbers in data
    if any(
        test_result == test_value
        for test_result in get_more_possible_results(test_numbers)
    )
)
