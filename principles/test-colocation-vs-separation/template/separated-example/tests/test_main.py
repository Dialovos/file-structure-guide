"""Tests for the separated-layout example.

The file name (``test_main.py``) mirrors the source file (``main.py``)
with the conventional ``test_`` prefix that pytest discovers by default.
The directory layout (`tests/` next to `src/`) is the separated pattern.
"""

from src.main import add, is_even


def test_add_returns_sum():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


def test_is_even():
    assert is_even(0) is True
    assert is_even(2) is True
    assert is_even(3) is False
