---
theme: seriph
background: https://freeforcommercialuse.net/images/c/0704/easter-eggs-background-1141.jpg
class: 'text-center'
highlighter: shiki
info: |
  ## Presentation about decorators in Python
  Made for my trial lesson for TeachMeSkills
---

# Decorators

---

# What are decorators in Python?

<v-clicks>

- Decorators are functions that modify the behavior of other functions and methods
- Introduced in [PEP-318](https://www.python.org/dev/peps/pep-0318/)
- Syntactic sugar: `@decorator`

</v-clicks>

---

# Functions as First Class Objects

#### A function in Python is an *object*

```python {0|1-3|4|4-5|6|6-7|all}
>>> def add_smile(text: str) -> str:
...     return text + " 🙂"
...
>>> type(add)
<class 'function'>
>>> add.__class__.__base__
<class 'object'>
```

---

# Functions as First Class Objects

#### You can store it in a variable

```python {1-3|4|5-8|9-10|all}
>>> def add_smile(text: str) -> str:
...     return text + " 🙂"
...
>>> smile_adder = add_smile
>>> print(add_smile)
<function add_smile at 0x7f8f0b4f9b10>
>>> print(smile_adder)
<function add_smile at 0x7f8f0b4f9b10>
>>> smile_adder("Hello")
'Hello 🙂'
```

---

# Functions as First Class Objects

#### You can pass it as an argument to another function

```python {1-3|4|4-7|4-9|all}
>>> def add_smile(text: str) -> str:
...     return text + " 🙂"
...
>>> smiled = map(add_smile, ["Hello", "Whats'up"])  # same as map(lambda x: x + " 🙂", ["Hello", "Whats'up"])
>>> for text in smiled:
...     print(text)
...
Hello 🙂
Whats'up 🙂
```

---

# Functions as First Class Objects

#### You can return it from a function

```python {2-4|5-7|8-12|13-16|17-21|all}
>>> from typing import Callable
>>> def add_smile(text: str) -> str:
...     return text + " 🙂"
...
>>> def add_mouthless(text: str) -> str:
...     return text + " 😶"
...
>>> def get_emoji(with_mouth: bool) -> Callable[[str], str]:
...     if with_mouth:
...         return add_smile
...     return add_mouthless
...
>>> get_emoji(True)
<function add_smile at 0x7f8f0b4f9b10>
>>> get_emoji(False)
<function add_mouthless at 0x7f8f0b4f9b10>
>>> get_emoji(True)("Hello")
'Hello 🙂'
>>> get_emoji(False)("No words")
'No words 😶'
```

---

# Our first decorator

Write a decorator that modifies the behavior of `add_smile` function:  
if text is emtpy, returns `😶` instead of adding ` 🙂` to the end

```python {1-2|4|5,1|6-8,2|9,5|all}
def add_smile(text: str) -> str:
    return text + " 🙂"

def decorate(func: Callable[[str], str]) -> Callable[[str], str]:
    def inner(text: str) -> str:
        if not text:
            return "😶"
        return func(text)
    return inner
```

```python {0|1|2-3|4-5|all}
>>> add_smile = decorate(add_smile)
>>> add_smile("Hello")
'Hello 🙂'
>>> add_smile("")
'😶'
```

---

# Syntactic sugar

```python
add_smile = decorate(add_smile)
```

With syntactic sugar

```python {0|all}
@decorate
def add_smile(text: str) -> str:
    return text + " 🙂"
```

---

# The great benefit: DRY code

We can use our decorator to decorate multiple functions avoiding repeated code

```python {2-3|2-3,6-7|2-3,6-7,10-11|all}
@decorate
def add_smile(text: str) -> str:
    return text + " 🙂"

@decorate
def add_snake(text: str) -> str:
    return text + " 🐍"

@decorate
def repeat(text: str) -> str:
    return f"{text} {text}"
```

```python {0|1-2|3-4|5-6|all}
>>> add_smile("")
'😶'
>>> add_snake("")
'😶'
>>> repeat("Hello")
'Hello Hello'
```

<!-- src/example1.py -->

---

# Another use case: validation

Write a decorator that validates `text` parameter and raises and error if text is empty


<div v-click>

```python
def validate_text(func: Callable[[str], str]) -> Callable[[str], str]:
    def inner(text: str) -> str:
        if not text:
          raise ValueError("Text cannot be empty!")
        return func(text)
    return inner
```

</div>

```python

def add_smile(text: str) -> str:
    return text + " 🙂"
```

<!-- src/example1.py -->

---

# Another use case: validation

Write a decorator that validates `text` parameter and raises and error if text is empty

```python
def validate_text(func: Callable[[str], str]) -> Callable[[str], str]:
    def inner(text: str) -> str:
        if not text:
          raise ValueError("Text cannot be empty!")
        return func(text)
    return inner
```

```python
@validate_text
def add_smile(text: str) -> str:
    return text + " 🙂"
```


<div v-click>

```python
>>> add_smile("")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: Text cannot be empty!
```

</div>

<!-- src/example1.py -->

---
---

# Common case: function execution timing

We wan't to print the execution time of a function

```python {0|1|2|3|4|5|6,5,3|7,4|8,1|all}
def timeit(func: Callable[[...], T]) -> Callable[[...], T]:
    def inner(*args, **kwargs) -> T:
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Execution time: {end - start}")
        return result
    return inner
```

<div v-click="[10, 13]">

```python
@timeit
def wait_one_second():
    time.sleep(1)
```

</div>

<div v-click="[11, 13]">

```python
>>> wait_one_second()
Execution time: 1.0002100467681885
```

</div>

<div v-click="[12, 13]">

```python
@timeit
def add_smile(text: str) -> str:
    return text + " 🙂"
```

</div>

---

# Commonly used built-in decorators

<v-clicks>

- [`@classmethod`](https://docs.python.org/3/library/functions.html#classmethod) & [`@staticmethod`](https://docs.python.org/3/library/functions.html#staticmethod)
- [`@property`](https://docs.python.org/3/library/functions.html#property)
- [`@cache`](https://docs.python.org/3/library/functools.html#functools.cache)
- [`@wraps`](https://docs.python.org/3/library/functools.html#functools.wraps)

</v-clicks>

---

# The name problem

```python


def validate(func: Callable[[str], str]) -> Callable[[str], str]:

    def inner(text: str) -> str:
        if not text:
            raise ValueError("Text can't be empty!")
        return func(text)
    return inner

@validate
def add_smile(text: str) -> str:
    return text + " 🙂"
```

<div v-click="[1, 3]">

```python
>>> print(add_smile)
```

</div>

<div v-click="[2, 3]">

```python
<function validate.<locals>.inner at 0x746a3b0899e0>
```

</div>

---

# The name problem solution: `@wraps`

```python
from functools import wraps

def validate(func: Callable[[str], str]) -> Callable[[str], str]:
    @wraps(func)
    def inner(text: str) -> str:
        if not text:
            raise ValueError("Text can't be empty!")
        return func(text)
    return inner

@validate
def add_smile(text: str) -> str:
    return text + " 🙂"
```

<div v-click="[1, 3]">

```python
>>> print(add_smile)
```

</div>

<div v-click="[2, 3]">

```python
<function add_smile at 0x746a3c3899e0>
```

</div>

<!-- src/example3.py -->

---

# Parametrized decorators

Create a decorator that makes decorated function return specific value
if one of specified exception occur during decorated function execution

```python {0|1|2|3-4|5-8|2-9|1-10|13-18|all}
def return_on_error(exceptions: tuple[Type[Exception], ...], returned_value: Any) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exceptions:
                return returned_value
        return inner
    return decorator

@return_on_error((ZeroDivisionError,), 0.0)
def divide(x: float, y: float) -> float:
    if x is None:
        raise ValueError("x cannot be None")
    if y is None:
        raise ValueError("y cannot be None")
    return x / y
```

<!-- src/example4.py -->

---

# Wrap up

<v-clicks>

- Decorators bases on the fact that functions are First Class Objects
- Decorator takes a function and returns another function
- Decorators may be simply called with function as parameter, or used with `@decorator` syntax
- We can use `functools.wraps` (which is also a decorator) to keep the metadata of decorated function accessible
- It is possible to create parametrized decorators in Python

</v-clicks>

---

# Exercises

1. Write a function that takes a list of numbers and returns sum of those numbers. Then create a decorator that will validate that every value in the list is a number and raise `TypeError` if not.
2. Write a parametrized decorator `retry_on_exception` that will retry a function `n` times if any of predefined exceptions occurs during function execution. Add ability to wait for certain number of seconds, which should also be a parameter of the decorator.
