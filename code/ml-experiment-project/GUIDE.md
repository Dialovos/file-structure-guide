## TL;DR

A **machine-learning experiment project** is organized around one loop: *change a config, run training, compare results*. Keep **code** (`src/<project>/`), **configuration** (`configs/`), **data** (`data/`, versioned by pointer, never by copy), and **run outputs** (`runs/<run-id>/`) in separate places. Every run is launched from a config file plus command-line overrides, seeds everything, and writes its config, metrics, and checkpoints into its own run directory, so any result can be traced to the exact code commit, config, and data version that produced it. Runs and checkpoints are **generated**, gitignored, and stored in an experiment tracker or object storage. This layout complements `cookiecutter-data-science` (which organizes the data pipeline and notebooks) with the parts that matter once you are training many models: configuration, run identity, and reproducibility.

## Principles & why

1. **A run is an immutable record.** Config, code revision, data version, seed, metrics, and artifacts are stored together under one run ID. Results without provenance can't be trusted or reproduced.
2. **Configuration is data, not code edits.** Hyperparameters and paths live in config files with explicit overrides; changing an experiment means changing a config, not editing a script.
3. **Code changes slowly, runs change quickly.** The library in `src/` is stable, reviewed, and tested; experiments are cheap and numerous. Keep their churn separate (see `stable-vs-volatile-separation`).
4. **Data is versioned by identity, not by copy.** Raw data is immutable and referenced by a hash or a pointer (see `large-files-and-binary-assets`), never duplicated into run directories.
5. **Determinism where possible, recorded where not.** Set and log seeds, library versions, and hardware notes; accept that some GPU operations are nondeterministic and record that too.
6. **Compare on shared ground.** Evaluation code, splits, and metric definitions live in one place, so runs are comparable across weeks.

## When to use

- **Training and fine-tuning projects** with more than a handful of runs.
- **Research code moving toward a paper or product**, where reproducibility matters.
- **Teams sharing a training codebase**, where configs and run records replace tribal knowledge.
- **Projects on a workstation or cluster** where long jobs run unattended and must record everything.

## When NOT to use

- **Exploratory analysis in notebooks.** Use `jupyter-research` until the work needs repeatable runs.
- **Data-pipeline-centric projects** without training loops; `cookiecutter-data-science` fits.
- **Serving and deployment code.** Model serving has its own layout (see `fastapi-project`); export the trained artifact and keep the serving repository separate.
- **One-off scripts.** A single `train.py` and a log is fine until you run the third variant.

## Tree diagram

```
project/
├── pyproject.toml
├── README.md
├── Makefile                          ← train, eval, lint, test entry points
├── configs/
│   ├── base.toml                     ← defaults shared by all runs
│   ├── experiment/
│   │   ├── baseline.toml
│   │   └── wider-model.toml          ← overrides only
│   └── data/
│       └── splits-v1.toml
├── src/
│   └── project/
│       ├── data.py                   ← loading, splits, transforms
│       ├── model.py
│       ├── train.py                  ← reads config, writes runs/<run-id>/
│       ├── evaluate.py
│       └── config.py                 ← loading and merging configs
├── tests/
│   ├── test_data.py
│   └── test_train_smoke.py           ← tiny run on fake data
├── data/
│   ├── raw.dvc                       ← pointer to immutable raw data
│   └── .gitignore                    ← real data paths, added by the tool
├── runs/                             ← gitignored: one directory per run
│   └── 2026-04-30-baseline-s0/
│       ├── config.resolved.toml
│       ├── metrics.jsonl
│       └── checkpoints/
├── reports/                          ← tracked summaries and figures
└── notebooks/                        ← exploration only, no pipeline logic
```

## Naming rules

- **Run IDs** are `YYYY-MM-DD-<config-name>-s<seed>` (for example `2026-04-30-wider-model-s0`), so they sort by date and say what they are. Add a short commit hash to the recorded metadata, not to the directory name.
- **Config files** are named for the experiment they describe (`baseline.toml`, `wider-model.toml`) and contain only differences from `base.toml`.
- **Config keys** are `snake_case` and grouped by section (`[model]`, `[optim]`, `[data]`).
- **Source modules** are `snake_case` and named for their role (`data.py`, `evaluate.py`).
- **Checkpoints** are `epoch-<n>.pt` or `step-<n>.pt` inside the run directory, plus `best.pt` and `last.pt` as pointers or copies.
- **Metric names** are consistent across runs (`val/loss`, `val/accuracy`), and defined once in `evaluate.py`.

## Worked example

A training script with hyperparameters typed into the source, results in `results_final2.csv`, and a model nobody can reproduce.

1. Extract every hyperparameter into `configs/base.toml`, and add `configs/experiment/baseline.toml` as an empty override.
2. Add `src/project/config.py` that loads `base.toml`, merges the experiment file, then applies `--set key=value` overrides, and returns one dictionary.
3. In `train.py`, create `runs/<date>-<name>-s<seed>/`, write `config.resolved.toml` (the fully merged config) and a `meta.json` with the git commit (`git rev-parse HEAD`), dirty flag, Python and library versions, and the data version, before training starts.
4. Seed `random`, NumPy, and the framework from the config seed, and log per-step metrics to `metrics.jsonl`.
5. Save checkpoints in `runs/<id>/checkpoints/`; gitignore `runs/`.
6. Add a smoke test that trains for two steps on synthetic data, so refactors can't silently break the pipeline: `pytest tests/test_train_smoke.py`.
7. Add `make train CONFIG=configs/experiment/wider-model.toml SEED=0`.
8. Compare runs by reading `metrics.jsonl` files (or an experiment tracker), and write conclusions into `reports/`.

Any past result can be reproduced from its run directory: check out the recorded commit, fetch the recorded data version, and run with the resolved config.

## Anti-patterns

- **Editing hyperparameters in source and committing "for the good run".** History no longer maps to results; use configs.
- **Overwriting a run directory** or reusing IDs. Runs are immutable; a rerun gets a new ID.
- **Committing checkpoints and datasets to git.** Use pointers or object storage (see `large-files-and-binary-assets`).
- **Notebook-only training** with state in cells. Fine for exploring, unfit as the source of a reported number.
- **Comparing runs on different splits or metric code.** Keep splits and metrics in shared, versioned modules.
- **Silent nondeterminism.** Record seeds, versions, and hardware; note when a result varies run to run.
- **`results_final_v3.csv` files.** Use run IDs and a tracker (see `versioning-in-paths`).

## Scaling & failure modes

- **Hundreds of runs**: file-per-run directories become hard to compare; add an experiment tracker (MLflow, Weights & Biases, or a lightweight local one) and keep `runs/` as the backing store.
- **Hyperparameter sweeps**: generate configs programmatically into `runs/` or a sweep tool's directory, with a shared sweep ID in the metadata.
- **Large data and checkpoints**: store in object storage, and log only URIs and hashes in the run record.
- **Multiple GPUs or nodes**: record world size and launcher command in `meta.json`, and keep one process responsible for writing run metadata.
- **Team use**: agree on run ID format and required metadata fields, and enforce them in `train.py`, not by convention.
- **Long-term storage**: prune old checkpoints by policy but keep configs and metrics forever; they are tiny.

## Variants

- **File-based runs** (this guide): plain directories and JSONL, no services needed.
- **Tracker-backed runs**: MLflow, Weights & Biases, or Aim store metrics and artifacts; the repository keeps configs and code.
- **Hydra-style configuration**: composable config groups and command-line overrides; layout changes to `conf/` with defaults lists.
- **DVC pipelines**: `dvc.yaml` declares stages and outputs, and `params.yaml` holds parameters; strong for reproducible pipelines with cached stages.
- **Package plus experiments repository**: a library repo with tests, and a separate repo that holds only configs and run records.

## Adoption checklist

- [ ] Every run writes its resolved config, git commit, dirty flag, seed, and data version before training.
- [ ] Hyperparameters live in config files, not in source.
- [ ] `runs/`, checkpoints, and datasets are gitignored and stored elsewhere by pointer.
- [ ] A smoke test trains for a few steps on synthetic data in CI.
- [ ] Splits and metric code are shared and versioned.
- [ ] Any reported number can be traced to a run directory and reproduced.

## Real-world projects using this

- **Cookiecutter Data Science** (Drivendata) covers data and notebook organization; see `code/cookiecutter-data-science/`.
- **Hydra** (Meta) documents composable configuration and output directories per run.
- **DVC** documents pipelines, `params.yaml`, and data versioning for reproducible experiments.
- **MLflow** and **Weights & Biases** document run tracking with parameters, metrics, and artifacts.
- **"Papers with Code" ML reproducibility checklist** and the **NeurIPS reproducibility checklist** list what a reproducible run should record.
- **Popular open-source training repositories** such as nanoGPT and torchtune show config-driven training scripts at different levels of structure.

## Migration & references

- **From an ad-hoc script:** extract configs, add run directories and metadata, then add the smoke test; leave results directories alone until you can regenerate them.
- **From `cookiecutter-data-science`:** keep `data/` and `notebooks/`, and add `configs/`, `runs/`, and a `train.py` that produces run records.
- **To a tracker:** keep the run directory layout and log the same fields to the tracker, so both stay consistent.
- **References:**
  - `code/cookiecutter-data-science/` and `code/jupyter-research/` for data and notebook layouts.
  - `principles/large-files-and-binary-assets/` for data and checkpoints.
  - `principles/stable-vs-volatile-separation/` for the code and runs split.
  - `code/python-uv-workspace/` or `code/python-src-layout/` for package structure.
