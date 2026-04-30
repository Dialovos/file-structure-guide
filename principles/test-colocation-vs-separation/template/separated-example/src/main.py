"""Trivial source module for the separated-layout example.

The matching test lives at ../tests/test_main.py — the test tree mirrors
the source tree by name. In a real project this file would sit at
``src/myapp/main.py`` and its test at ``tests/myapp/test_main.py``.
"""


def add(a: int, b: int) -> int:
    """Return the sum of two integers."""
    return a + b


def is_even(n: int) -> bool:
    """Return True iff ``n`` is even."""
    return n % 2 == 0
