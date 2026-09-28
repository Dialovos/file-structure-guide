## TL;DR

**Cookiecutter Data Science** (CCDS) is the most widely adopted layout convention for data-science / machine-learning projects. Drivendata published it in 2015 as a `cookiecutter` template; the v2 rewrite (released 2024) modernised the tooling but kept the load-bearing directory structure. The structure says: **immutable raw data goes in `data/raw/`, never edited, never committed; derived data goes in `data/{interim, processed, external}/`; exploratory analysis lives in `notebooks/` with files named `<order>-<initials>-<purpose>.ipynb`; reusable Python lives in an installable package under `src/<project>/`; trained models go in `models/`; figures and write-ups go in `reports/`; and a `Makefile` orchestrates the pipeline.** The split between throwaway notebooks and reusable `src/` is the heart of CCDS — it forces "promotion" from notebook to library when a function gets reused, instead of letting copy-pasted cells proliferate. The naming convention for notebooks (`0.1-jh-eda.ipynb`, `1.0-jh-feature-eng.ipynb`, etc.) is opinionated but practical: the leading number gives you ordering, the initials give you authorship in a multi-person team, the purpose tells future-you what's in there. CCDS is a *cookiecutter* template, but you don't need cookiecutter to use the layout — `cp -r`-ing this guide's `template/` works fine. The single biggest win: any data scientist who has worked on a CCDS project knows where things are in any other CCDS project, instantly.

## Principles & why

CCDS is shaped by six principles, each backed by a directory or convention.

1. **Raw data is sacred and never committed.** `data/raw/` contains the original, immutable downloads. Once written, never edit. Never commit (it's gitignored except for `.gitkeep`). If you mess up `data/processed/`, you can rerun the pipeline from `data/raw/`. If `data/raw/` is gone, the project is unreproducible.
2. **Pipelines are the source of truth, not notebooks.** A CCDS project should be reproducible from `make data && make features && make train`. Notebooks are exploration; `src/<project>/` and the `Makefile` are production. If a notebook produces a useful figure or model, the *code* gets promoted into `src/`, the notebook gets archived.
3. **`src/<project>/` is an installable Python package.** Not a script directory. With `pip install -e .` (or `uv pip install -e .`) the package is importable from anywhere — including from notebooks (`from project.features import build_features`). This is the critical move that lets notebooks evolve without circular imports or `sys.path` hacks.
4. **Notebooks are numbered, named, and dated by intent.** `0.1-initials-eda.ipynb` (`0.x` is exploration), `1.0-initials-feature-engineering.ipynb` (`1.x` is feature work), `2.0-initials-modeling.ipynb` (`2.x` is models). The leading number sorts files in a sensible execution order; the initials assign authorship; the suffix says what the notebook does. Re-runnable order is implicit in the filenames.
5. **Configuration belongs in code, in `pyproject.toml`, or in `Makefile`, not in notebooks.** Hardcoded paths, magic numbers, and dataset URLs go into `src/<project>/config.py` or as environment variables read in the `Makefile`. Notebooks `import` configuration — they don't define it.
6. **The Makefile is the contract.** `make data`, `make features`, `make train`, `make clean`, `make lint`, `make test`. Anyone — including the data scientist who joins next week — runs `make` to know what targets exist. CI runs `make`. The Makefile is the first place a stranger to your project looks.

A seventh, softer principle: **`reports/figures/` is where polished outputs go.** Throwaway plots stay in notebooks. The figure that goes in the paper / slide deck / dashboard gets saved into `reports/figures/<date>-<purpose>.png` so it's reproducible and survives notebook edits.

## When to use

- **ML / DS projects with intent to productionize.** Even early-stage. The structure pays off the first time someone needs to reproduce your work.
- **Reproducible research.** Anything where "rerun the pipeline" needs to be a one-liner.
- **Multi-person DS teams.** The shared convention is the single biggest collaboration win — everyone knows where to look.
- **Projects where data, code, and model are all evolving.** The clean separation of `data/`, `src/`, `models/`, `notebooks/` keeps each domain isolated.
- **Course / tutorial projects.** Made With ML, fast.ai, and similar curricula often standardise on CCDS.

## When NOT to use

- **Pure notebook exploration with no productionization in sight.** Use `code/jupyter-research/` instead — lighter weight, no `src/` to maintain.
- **Production ML platforms** (AWS SageMaker, Vertex AI, Azure ML). They have their own opinionated layouts (model registries, training jobs, deployment configs) that don't fit CCDS cleanly.
- **Single-script analyses.** A 200-line `analysis.py` doesn't need `data/raw/`, `data/interim/`, `data/processed/`, `notebooks/`, `models/`, etc.
- **Heavy-pipeline projects** where DVC, Kedro, or Airflow is the right tool. CCDS works with DVC (and ships DVC-flavored variants), but Kedro is a deeper opinion that subsumes much of CCDS.
- **Real-time / streaming systems.** CCDS assumes a batch pipeline (raw → interim → processed → model). Streaming changes the data flow.

## Tree diagram

```
project/
├── pyproject.toml          ← or requirements.txt + setup.py (CCDS v2 vs v1)
├── README.md
├── LICENSE
├── .gitignore
├── Makefile                ← `make data`, `make features`, `make train`
├── data/
│   ├── raw/                ← immutable, never committed; .gitkeep only
│   ├── interim/
│   ├── processed/
│   └── external/
├── docs/
├── models/                 ← trained model artifacts (often gitignored)
├── notebooks/              ← exploration; named `0.1-initials-purpose.ipynb`
│   └── 0.1-jh-eda.ipynb
├── references/
├── reports/
│   └── figures/
├── src/                    ← installable package
│   └── project/
│       ├── __init__.py
│       ├── data/
│       │   └── make_dataset.py
│       ├── features/
│       │   └── build_features.py
│       ├── models/
│       │   ├── train_model.py
│       │   └── predict_model.py
│       └── visualization/
└── tests/
```

## Naming rules

- **Top-level directory**: kebab-case for the *repo* (`my-classifier-project/`); the *Python package* inside `src/` is snake_case (`src/my_classifier/` or just `src/project/` for a generic name). PEP 8 is non-negotiable for the package name.
- **Notebooks**: `<step>.<sub-step>-<initials>-<short-description>.ipynb`. Examples: `0.1-jh-eda.ipynb`, `1.0-jh-feature-engineering.ipynb`, `2.1-mn-modeling-randomforest.ipynb`. Initials let multi-author teams keep notebook ownership clear.
- **Data files**: descriptive snake_case + extension. `customers_2024_q3.csv`, `train_processed.parquet`. Avoid spaces.
- **Models**: snake_case + extension reflecting the format. `random_forest_v2.pkl`, `xgboost_baseline.json`, `bert_finetuned.bin`. Versioning in the filename when the model registry isn't formal.
- **Figures in `reports/figures/`**: `YYYY-MM-DD-<purpose>.png`. `2026-04-30-feature-importances.png`. Date-prefixed so chronological order is built-in.
- **Python module names**: lowercase, snake_case, descriptive. `make_dataset.py`, `build_features.py`, `train_model.py`. Avoid generic names like `utils.py` at the top of a package — push them into a sub-package or rename for purpose.
- **Makefile targets**: lowercase, hyphen-free verbs or noun-phrases. `data`, `features`, `train`, `clean`, `lint`, `test`. Multi-word targets use hyphens: `clean-data`, `train-baseline`.

## Worked example

A notebook `final_analysis_v3.ipynb` reads `../Downloads/data.csv` and cleaned data is written next to it.

1. Scaffold with `ccds` (or copy the layout) so `data/{raw,interim,processed,external}/` exist.
2. Move the original file to `data/raw/` and treat it as read-only (`chmod -R a-w data/raw`).
3. Move cleaning code out of the notebook into `src/<project>/data/make_dataset.py`; the notebook now `import`s it (`pip install -e .`).
4. Rename notebooks to `<order>-<initials>-<purpose>.ipynb`, for example `1.0-jh-eda.ipynb`.
5. Add `make data`, `make features`, `make train` targets so the pipeline reruns from raw with one command.
6. Gitignore `data/` contents and `models/`; keep `.gitkeep` files.

Anyone can now reproduce `data/processed/` from `data/raw/` without opening a notebook.

## Anti-patterns

- **Editing `data/raw/`.** The whole point of `data/raw/` is that it's immutable. If you need to clean / filter / transform, write the result to `data/interim/` (work-in-progress) or `data/processed/` (final).
- **Committing data to git.** Even small CSVs grow. Use `.gitkeep` to track the empty directories; gitignore everything else. Real data lives in S3 / GCS / DVC-tracked storage.
- **Notebooks that hardcode paths like `'/Users/jane/data/foo.csv'`.** Breaks for everyone else immediately. Use `pathlib.Path(__file__).parent / "data" / "raw" / "foo.csv"` or a path constant in `src/project/config.py`.
- **`sys.path.append('../')` in notebooks** to import from `src/`. Skip the hack: install the package once with `pip install -e .` and just `from project.features import build_features`.
- **Duplicating utility functions across notebooks.** As soon as you copy-paste a function from one notebook to another, promote it to `src/<project>/`. Notebooks should import from the package.
- **`notebooks/Untitled.ipynb`, `notebooks/Untitled1.ipynb`, ...** Rename immediately. The CCDS naming convention is half the value of CCDS.
- **Committing `*.ipynb_checkpoints/`.** Add to `.gitignore`. `nbstripout` (a pre-commit hook) is also worth installing — it strips notebook outputs on commit so diffs are sane.
- **Skipping the `Makefile`.** "I'll just run the scripts directly." Six months later nobody (including you) remembers the order. Make the Makefile from day one.
- **Dropping models in the repo root** (`final_model.pkl` next to `README.md`). Goes in `models/`, gitignored unless tiny, ideally tracked by DVC or MLflow.
- **Notebooks in `src/`.** `src/` is for installable code only. Notebooks in `notebooks/`. They have different lifecycles.

## Scaling & failure modes

- **Large raw data** doesn't belong in git. Use DVC, git-lfs, or an object store with a manifest of checksums committed to the repo.
- **Notebook drift**: notebooks stay for exploration; the second time code is copied between notebooks, promote it to `src/`.
- **Experiment sprawl** (many models, many runs) outgrows `models/`. Add an experiment tracker (MLflow, Weights & Biases) rather than folders like `models/v2/`.
- **Collaboration**: strip notebook outputs before commit (`nbstripout`) so diffs are readable.

## Variants

- **CCDS v2 (this guide)** — `pyproject.toml`-based, `hatchling` or `setuptools` backend, `uv` or `pip-tools` for env, optional Hydra for config. Released 2024. Current default.
- **CCDS v1** — older `setup.py` + `requirements.txt` style, plain `pip`. Still in widespread use; functionally equivalent in layout.
- **CCDS + DVC** — adds `.dvc/` and uses DVC to version `data/` and `models/`. Pipeline definitions in `dvc.yaml`. Drivendata maintains a DVC-flavored variant.
- **CCDS + MLflow** — same layout, but `models/` is replaced (or supplemented) by an MLflow tracking server. Common in production teams.
- **Kedro** — a deeper opinion that swallows a lot of CCDS's structure but adds a pipeline framework, a data catalog (`conf/base/catalog.yml`), and Hooks. If your project is more "engineering" than "research," Kedro often wins.
- **Pyro / nf-core / similar domain-specific** — bioinformatics / scientific-computing communities have CCDS-shaped templates with extra directories. Same shape, just specialised.
- **Just the layout, no cookiecutter** — copy `template/` and run with it. CCDS is a convention more than a tool; many teams skip the cookiecutter prompt and just maintain the structure manually.

## Adoption checklist

- [ ] `data/raw/` is read-only, ignored by git, and has a documented source.
- [ ] `make data && make features` reproduces `data/processed/` from raw.
- [ ] Notebooks are numbered and import shared code from `src/`.
- [ ] Notebook outputs are stripped in a pre-commit hook.
- [ ] A README section says how to obtain the raw data.

## Real-world projects using this

- **drivendata/cookiecutter-data-science** — the original. The repo itself is the canonical reference.
- **Made With ML** (`GokuMohandas/Made-With-Ml`) — Goku Mohandas's MLOps curriculum; the project structure is a pragmatic CCDS variant.
- **Drivendata competition winners** — many published Kaggle / Drivendata solutions follow CCDS by default.
- **NeurIPS reproducibility-track repos** — increasingly use CCDS or close-cousin layouts.
- **fast.ai's industrial projects** — Jeremy Howard's project repos lean toward notebook-heavy variants but borrow CCDS conventions for `data/` and `src/`.
- **Cloudera Fast Forward Labs** — research-engineering reports often ship in CCDS form.
- **Spotify, Stripe, and other industry teams' public DS examples** — many internal data-science tooling teams converged on CCDS-shaped layouts independently and now publish blog posts using CCDS as the reference.

## Migration & references

- **From a flat `analysis.ipynb` + `data.csv` repo to CCDS**: create `data/raw/`, `git mv data.csv data/raw/`, gitignore `data/raw/*` (keep `.gitkeep`). Create `notebooks/`, `git mv analysis.ipynb notebooks/0.1-<initials>-eda.ipynb`. Create `src/<project>/`, `pip install -e .`, start promoting reusable functions out of the notebook.
- **From CCDS v1 to v2**: replace `setup.py` + `requirements.txt` with a single `pyproject.toml` (use `hatchling` or `setuptools` backend). Move dependencies into `[project] dependencies = [...]`. The directory layout is unchanged.
- **Adding DVC**: `dvc init`, `dvc add data/raw/<file>`. DVC tracks the file and stores the actual data in `.dvc/cache/` + remote storage; `git` only sees a small `.dvc` pointer file.
- **Adding a new pipeline stage**: add a target to `Makefile` (e.g. `evaluate: train ... ; python -m project.models.evaluate`). Add the implementation in `src/project/models/evaluate.py`. Update the README.
- **Switching from `pip` to `uv`**: `uv venv`, `uv pip install -e .`. Drop-in faster pip; CCDS v2 ships with this in mind.
- **References**:
  - drivendata.org/blog/ccds-v2/ — release post for CCDS v2 with rationale.
  - cookiecutter-data-science.drivendata.org — current docs.
  - Made With ML — Goku Mohandas's project structure tutorial (madewithml.com).
  - Sibling guides: `code/jupyter-research/` (notebooks-only sibling), `code/python-src-layout/` (the underlying Python convention CCDS builds on).
