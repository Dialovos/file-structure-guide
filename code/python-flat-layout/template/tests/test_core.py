"""Starter tests for mypackage.core.

In flat-layout, these tests can run without ``pip install -e .`` as
long as you invoke pytest from the repo root — the package directory
is already on ``sys.path``. Installing is still recommended so that
console scripts (``mypackage`` from the shell) work.
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
