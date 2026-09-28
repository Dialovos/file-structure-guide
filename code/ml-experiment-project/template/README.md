# ml-experiment-project — template

A dependency-free skeleton (standard library only) that shows the run-directory pattern: merged config, metadata, seeded run, metrics file.

## What to rename

- `project` package name in `src/project/` and `pyproject.toml`

## What to fill

- `configs/base.toml` — your real hyperparameters
- `src/project/train.py` — replace the fake training loop with your framework

## What to delete

- The fake loop and its smoke test once you have a real model

## First run

```bash
pip install -e .
make train CONFIG=configs/experiment/baseline.toml SEED=0
pytest
```

## Pair this with

- `../GUIDE.md` — the reasoning
- `../../cookiecutter-data-science/` — data and notebook layout
