"""Core logic for mypackage.

This module is the public API surface. Keep it small; push internal
helpers into private modules (`_helpers.py`) and re-export only what
callers should rely on.
"""

from __future__ import annotations


def greet(name: str) -> str:
    """Return a friendly greeting.

    Replace this stub with real logic. The signature exists so that
    the starter test in ``tests/test_core.py`` has something to call.

    Parameters
    ----------
    name:
        Name of the person or thing to greet. Must be non-empty.

    Returns
    -------
    str
        A greeting string of the form ``"Hello, {name}!"``.

    Raises
    ------
    ValueError
        If ``name`` is empty after stripping whitespace.
    """
    cleaned = name.strip()
    if not cleaned:
        raise ValueError("name must not be empty")
    return f"Hello, {cleaned}!"
