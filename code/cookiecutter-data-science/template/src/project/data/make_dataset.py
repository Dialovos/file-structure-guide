"""Turn raw data (data/raw/) into a processed dataset (data/processed/).

Run from the repo root:
    python -m project.data.make_dataset data/raw data/processed
or via:
    make data
"""

from __future__ import annotations

from pathlib import Path

import click


@click.command()
@click.argument("input_filepath", type=click.Path(exists=True, file_okay=True, dir_okay=True))
@click.argument("output_filepath", type=click.Path(file_okay=True, dir_okay=True))
def main(input_filepath: str, output_filepath: str) -> None:
    """Read raw data from INPUT_FILEPATH, write processed data to OUTPUT_FILEPATH."""
    inp = Path(input_filepath)
    out = Path(output_filepath)
    out.mkdir(parents=True, exist_ok=True)
    click.echo(f"[make_dataset] reading from {inp}, writing to {out}")
    # Real implementation: load raw, clean, save to processed.


if __name__ == "__main__":
    main()
