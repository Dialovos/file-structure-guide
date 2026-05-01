"""Command-line entry point for mypackage.

Wired up via ``[project.scripts]`` in ``pyproject.toml``. Run as
``python -m mypackage`` (after adding a ``__main__.py``) or as
``mypackage`` once the package is installed.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from .core import greet


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mypackage",
        description="Stub CLI for mypackage. Replace with real commands.",
    )
    parser.add_argument(
        "name",
        nargs="?",
        default="world",
        help="Who to greet (default: world).",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        print(greet(args.name))
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
