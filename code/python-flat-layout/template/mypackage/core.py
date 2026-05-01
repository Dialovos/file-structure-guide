"""Core logic for mypackage.

Replace the ``greet`` stub with the real public API. Keep imports
explicit; avoid ``from .other import *``.
"""

from __future__ import annotations


def greet(name: str) -> str:
    """Return a friendly greeting.

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
