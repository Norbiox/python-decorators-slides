#!/usr/bin/env python3
# pylint: disable=missing-docstring  # type: ignore
import time
from typing import Callable, TypeVar

T = TypeVar("T")


def timeit(func: Callable[[...], T]) -> Callable[[...], T]:
    def inner(*args, **kwargs) -> T:
        start = time.time()
        result: T = func(*args, **kwargs)
        end = time.time()
        print(f"Execution time: {end - start}")
        return result

    return inner


@timeit
def wait_one_second():
    time.sleep(1)


@timeit
def wait_and_print(text: str):
    time.sleep(1)
    print(text)


if __name__ == "__main__":
    wait_one_second()
    wait_and_print("Hello")
