"""Starter tests for mypackage.core.

These tests import from the *installed* package (`mypackage`), not
from `src/`. Run after `pip install -e .[dev]`.
"""

from __future__ import annotations

import pytest

from mypackage.core import greet


def test_greet_returns_friendly_string() -> None:
    assert greet("Ada") == "Hello, Ada!"


def test_greet_strips_whitespace() -> None:
    assert greet("  Ada  ") == "Hello, Ada!"


def test_greet_rejects_empty_name() -> None:
    with pytest.raises(ValueError):
        greet("   ")
