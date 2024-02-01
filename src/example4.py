#!/usr/bin/env python3
# pylint: disable=missing-docstring
from functools import wraps
from typing import Callable, Type, TypeVar

T = TypeVar("T")


def return_on_error(
    exceptions: tuple[Type[Exception], ...], returned_value: T
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def inner(*args, **kwargs) -> T:
            try:
                return func(*args, **kwargs)
            except exceptions:
                return returned_value

        return inner

    return decorator


@return_on_error((ZeroDivisionError,), 0.0)
def divide(x: int | float, y: int | float) -> float:
    if x is None:
        raise ValueError("x can't be None!")
    if y is None:
        raise ValueError("y can't be None!")
    return x / y


if __name__ == "__main__":
    print(divide(4, 2))
    print(divide(4, 0))
    print(divide(4, None))
