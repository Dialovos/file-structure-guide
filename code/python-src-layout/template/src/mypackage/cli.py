"""Command-line entry point for mypackage.

Wired up via ``[project.scripts]`` in ``pyproject.toml``. After
``pip install -e .`` you can run ``mypackage <name>`` from any shell.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from .core import greet


def build_parser() -> argparse.ArgumentParser:
    """Construct the top-level argument parser."""
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
    """Run the CLI. Returns a process exit code."""
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
