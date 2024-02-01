#!/usr/bin/env python3
# pylint: disable=missing-docstring
from typing import Callable


def decorate(func: Callable[[str], str]) -> Callable[[str], str]:
    def inner(text: str) -> str:
        if not text:
            # return "😶"
            raise ValueError("Text can't be empty!")
        return func(text)

    return inner


@decorate
def add_smile(text: str) -> str:
    return text + " 🙂"


@decorate
def add_snake(text: str) -> str:
    return text + " 🐍"


@decorate
def repeat(text: str) -> str:
    return f"{text} {text}"


if __name__ == "__main__":
    print(add_smile("Hello"))
    print(add_snake("Hello"))
    print(repeat("Hello"))

    print(add_smile(""))
    print(add_snake(""))
    print(repeat(""))
