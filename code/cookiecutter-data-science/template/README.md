# Cookiecutter Data Science (CCDS) — template

A `cp -r`-able starter for a CCDS-flavored ML/DS project. Raw data
in `data/raw/` (immutable), notebooks in `notebooks/` (numbered),
reusable code in `src/project/` (installable package), trained
models in `models/`, polished outputs in `reports/`. Driven by a
`Makefile`.

## What lives where

- **`data/raw/`** — immutable, never edited, never committed (only
  `.gitkeep`). Drop the original CSVs / parquet / archives here.
- **`data/interim/`** — work-in-progress derived data.
- **`data/processed/`** — final, model-ready data.
- **`data/external/`** — third-party data (lookup tables, joins).
- **`notebooks/`** — exploration. Rename `0.1-initials-eda.ipynb` to
  your initials. Add new notebooks with the
  `<step>.<sub>-<initials>-<purpose>.ipynb` convention.
- **`src/project/`** — installable Python package. `pip install -e .`
  once, then `from project.features import build_features` works
  from anywhere (notebooks, scripts, tests).
- **`src/project/data/make_dataset.py`** — entrypoint for `make data`.
- **`src/project/features/build_features.py`** — entrypoint for
  `make features`.
- **`src/project/models/{train,predict}_model.py`** — entrypoints
  for `make train` and inference.
- **`src/project/visualization/visualize.py`** — plot helpers.
- **`models/`** — trained-model artifacts. Gitignored except
  `.gitkeep`.
- **`reports/figures/`** — polished, paper-ready figures. Date-prefix
  filenames: `2026-04-30-feature-importances.png`.
- **`Makefile`** — pipeline contract. `make data && make features &&
  make train` reproduces the project from `data/raw/`.
- **`tests/`** — pytest tests for `src/project/`.

## What to rename

- `pyproject.toml` `[project] name`: replace `project` with the
  Python-package name (snake_case).
- `src/project/` directory: rename to match the package name.
- `pyproject.toml` `[tool.hatch.build.targets.wheel] packages`:
  update the path if you renamed `src/project/`.
- `Makefile` `python -m project.*` calls: update to the new package
  name.
- `LICENSE` `{{YEAR}}` and `{{NAME}}`.

## First run

```bash
make requirements                         # pip install -e .[dev]
make data                                 # raw -> processed
make features                             # processed -> features
make train                                # features -> model
make test                                 # pytest
make lint                                 # ruff
```

If you don't have `make`, run the equivalent commands directly:

```bash
pip install -e ".[dev]"
python -m project.data.make_dataset data/raw data/processed
python -m project.features.build_features
python -m project.models.train_model
```

## Notebook workflow

1. Rename `notebooks/0.1-initials-eda.ipynb` to your initials.
2. New notebooks go alongside it with the
   `<step>.<sub>-<initials>-<purpose>.ipynb` naming.
3. As soon as a notebook function gets reused, *promote* it into
   `src/project/`. Notebooks `import`, they don't define.
4. Save polished figures into `reports/figures/` (the
   `visualize.save_figure` helper is a starting point).

## Pair this with

- `../GUIDE.md` — full reasoning behind this layout, including
  variants (DVC, MLflow, Kedro).
- `../jupyter-research/` — the lighter-weight notebooks-only sibling.
- `../python-src-layout/` — the underlying Python convention CCDS
  builds on.
- The CCDS docs at cookiecutter-data-science.drivendata.org —
  canonical reference.
