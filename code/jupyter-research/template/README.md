# Jupyter research — template

A `cp -r`-able starter for a notebooks-first research project.
Numbered notebooks in `notebooks/`, two-tier data lifecycle, dated
figures, optional LaTeX paper, optional utility `src/`.

## What lives where

- **`notebooks/`** — the canonical artifact. Numbered for execution
  order (`01-data-loading.ipynb`, `02-eda.ipynb`, ...). Always
  *Restart Kernel and Run All* before committing.
- **`data/raw/`** — original, immutable, gitignored. Drop the source
  CSVs / parquet / archives here; document where they came from in
  the README.
- **`data/processed/`** — derived data; gitignored.
- **`figures/`** — polished, paper-ready figures. Date-prefix
  filenames: `2026-04-30-eda-distributions.png`.
- **`paper/`** — *optional*. LaTeX (`main.tex` + `references.bib`)
  for the write-up. Build with `latexmk -pdf paper/main.tex`.
- **`src/`** — *optional*. Utility code reused across notebooks.
  Install once with `pip install -e .` so notebooks can
  `from src.utils import project_root`. Rename `src/` to a real
  package name (e.g. `research_utils/`) when the project grows.

If you don't have a paper or shared utilities, delete `paper/`
and `src/`.

## What to rename

- `pyproject.toml` `[project] name`: replace `research-project`.
- `paper/main.tex` title, author, abstract.
- `LICENSE` `{{YEAR}}` and `{{NAME}}`.

## First run

```bash
pip install -e ".[dev]"          # installs research_utils + nbstripout/jupytext
jupyter lab notebooks/           # open the notebooks
```

For pure conda users, replace `pyproject.toml` with `environment.yml`
and `conda env create -f environment.yml`.

## Notebook hygiene

```bash
nbstripout --install            # strip outputs on every git add
```

Then commit `.ipynb` files freely without leaking outputs into the
diff.

For top-to-bottom reproducibility:

```bash
jupyter nbconvert --to notebook --execute notebooks/*.ipynb \
    --output-dir notebooks/_executed
```

CI can run this and fail if any notebook throws.

## Adding a new notebook

1. Pick the next two-digit prefix.
2. `cp notebooks/02-eda.ipynb notebooks/05-validation.ipynb` then
   rewrite.
3. Use the relative-path conventions (`Path('..') / 'data' / ...`).
4. Save figures to `figures/<today>-<purpose>.png`.

## Pair this with

- `../GUIDE.md` — full reasoning behind this layout, including
  Quarto and Jupyter Book variants.
- `../cookiecutter-data-science/` — heavier-weight sibling for
  projects with intent to productionize.
- `../python-src-layout/` — the underlying Python convention if
  `src/` grows.
