#!/usr/bin/env python3
# pylint: disable=missing-docstring
from functools import wraps
from typing import Callable


def validate(func: Callable[[str], str]) -> Callable[[str], str]:
    # @wraps(func)
    def inner(text: str) -> str:
        if not text:
            raise ValueError("Text can't be empty!")
        return func(text)

    return inner


@validate
def add_smile(text: str) -> str:
    return text + " 🙂"


if __name__ == "__main__":
    print(add_smile)
