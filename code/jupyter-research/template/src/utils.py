"""Small helpers shared across notebooks.

Promote any function that gets reused in 2+ notebooks into this
file. Notebooks `from src.utils import ...`; they should not
redefine helpers locally.
"""

from __future__ import annotations

from pathlib import Path


def project_root() -> Path:
    """Return the absolute path to the project root.

    Resolves from this file's location, so it works regardless of
    where a notebook or script is invoked from.
    """
    return Path(__file__).resolve().parent.parent
