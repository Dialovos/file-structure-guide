"""Command-line interface."""
import sys

from acme_core import greet


def main() -> None:
    print(greet(sys.argv[1] if len(sys.argv) > 1 else "world"))
