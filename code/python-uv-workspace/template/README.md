# python-uv-workspace — template

A virtual uv workspace with a library and a CLI that depends on it.

## What to rename

- `acme` prefix in package names and import packages to your own
- `acme_core`/`acme_cli` directories under `src/` (import names are `snake_case`)

## What to fill

- Root `pyproject.toml` — tool settings and dev group
- Each member's `pyproject.toml` — description, dependencies, URLs

## What to delete

- The `greet()` example and its test once you have real code

## First run

```bash
uv sync --all-packages
uv run pytest
```

## Pair this with

- `../GUIDE.md` — the reasoning
- `../../python-src-layout/` — the per-package layout
